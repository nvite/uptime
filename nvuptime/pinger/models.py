import datetime

import pytz

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from dirtyfields import DirtyFieldsMixin

from nvuptime.pinger.email import (EndpointDownEmailThread,
                                   EndpointUpEmailThread)

PASS = 0
TIMEOUT = 1
MISMATCH = 2
ERROR = 3
DISPOSITION_CHOICES = (
    (PASS, 'Passed'),
    (TIMEOUT, 'Timed out'),
    (MISMATCH, 'Failed content'),
    (ERROR, 'Failed'),
)

OUTAGE_THRESHOLD = 3
DISRUPTION = 0
WATCHING = 1
RESOLVED = 2
OUTAGE_STATUS_CHOICES = (
    (DISRUPTION, 'Disruption'),
    (WATCHING, 'Watching'),
    (RESOLVED, 'Resolved'),
)


class GroupManager(models.Manager):
    use_for_related_fields = True

    def active(qset):
        return qset.filter(is_active=True)


class Group(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, unique=True, max_length=100)
    is_active = models.BooleanField(default=False)
    members = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GroupManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super(Group, self).save(*args, **kwargs)

    def ensure_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)[:100].rstrip('-')


class EndpointManager(models.Manager):
    use_for_related_fields = True

    def active(qset):
        return qset.filter(is_active=True)


class Endpoint(DirtyFieldsMixin, models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, unique=True, max_length=100)
    url = models.URLField()
    ping_interval = models.DurationField(default=datetime.timedelta(minutes=5))
    timeout = models.DurationField(default=datetime.timedelta(seconds=5))
    expected_status = models.SmallIntegerField()
    expected_text = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(db_index=True, default=True)
    is_up = models.BooleanField(db_index=True, default=True)
    group = models.ForeignKey(Group, related_name='endpoints')
    subscribers = models.ManyToManyField(User, related_name='endpoints',
                                         blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EndpointManager()

    def __str__(self):
        return self.title

    @property
    def ping_count(self):
        return self.pings.count()

    @property
    def success_rate(self):
        try:
            return self.pings.passed().count() / self.pings.all().count()
        except:
            pass

    @property
    def success_rate_today(self):
        try:
            today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            pings_today = self.pings.exclude(created_at__lt=today_min).count()
            success_pings_today = self.pings.passed().exclude(created_at__lt=today_min).count()
            if pings_today == 0:
                success_rate = 1
            else:
                success_rate = success_pings_today / pings_today

            return success_rate

        except:
            pass

    @property
    def success_rate_last_week(self):
        try:
            week_ago = timezone.now()-timedelta(days=7)
            pings_last_week = self.pings.exclude(created_at__lt=week_ago).count()
            success_pings_last_week = self.pings.passed().exclude(created_at__lt=week_ago).count()
            if pings_last_week == 0:
                success_rate = 1
            else:
                success_rate = success_pings_last_week / pings_last_week

            return success_rate

        except:
            pass

    @property
    def avg_response_time(self):
        try:
            return self.pings.passed().aggregate(
                Avg('response_time'))['response_time__avg']
        except:
            pass

    @property
    def age(self):
        return (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) -
                self.pings.latest().created_at)

    @property
    def is_due(self):
        if not self.pings.latest():
            return True
        return self.age >= self.ping_interval

    def save(self, *args, **kwargs):
        self.ensure_slug()

        dirty_fields = self.get_dirty_fields()
        if 'is_up' in dirty_fields.keys():
            if self.is_up is False:
                EndpointDownEmailThread(self).run()
            else:
                EndpointUpEmailThread(self,).run()

        super(Endpoint, self).save(*args, **kwargs)

    def ensure_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)[:100].rstrip('-')


class PingManager(models.Manager):
    use_for_related_fields = True

    def passed(qset):
        return qset.filter(disposition=PASS)

    def failed(qset):
        return qset.filter(disposition__gt=PASS)

    def latest(qset):
        return qset.order_by('-created_at').first()

    def timeframe(qset, **kwargs):
        pass


class Ping(models.Model):
    endpoint = models.ForeignKey(Endpoint, related_name='pings')
    created_at = models.DateTimeField(auto_now_add=True)
    disposition = models.SmallIntegerField(db_index=True,
                                           choices=DISPOSITION_CHOICES)
    response_time = models.DecimalField(decimal_places=6, max_digits=10)
    response_code = models.SmallIntegerField(db_index=True)
    response_headers = models.TextField()
    response = models.TextField()

    objects = PingManager()

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        data = self.__dict__
        data['endpoint'] = self.endpoint.__str__()
        data['disposition'] = self.get_disposition_display()
        return "{endpoint}: {disposition}@{created_at}".format(**data)


class OutageManager(models.Manager):
    use_for_related_fields = True

    def active(qset):
        return qset.filter(end=None)

    def already_down(qset):
        return qset.filter(end=None).count() > 0


class Outage(models.Model):
    title = models.CharField(max_length=255, default='Failed Automated System Checks')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    objects = OutageManager()

    class Meta:
        ordering = ('-start', )

    def __str__(self):
        data = self.__dict__
        data['duration_minutes'] = int(self.duration.total_seconds() / 60)
        return "{title} ({duration_minutes}m)".format(**data)

    @property
    def duration(self):
        end = self.end or datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        return end - self.start

    @property
    def is_active(self):
        return self.end is None


class OutageUpdate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(db_index=True,
                                      choices=OUTAGE_STATUS_CHOICES)
    text = models.TextField(default='We are actively investigating a service disruption and will post more information when available.')
    outage = models.ForeignKey(Outage, related_name='updates')

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        data = self.__dict__
        data['outage'] = self.outage.__str__()
        data['status'] = self.get_status_display()
        return "{created_at} {outage} updated to {status}: {text}".format(**data)
