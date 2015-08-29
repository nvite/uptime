import datetime

from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, unique=True, max_length=100)
    members = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"{name}".format(self.__dict__)

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super(Group, self).save(*args, **kwargs)

    def ensure_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)[:100].rstrip('-')


class EndpointManager(models.Manager):
    use_for_related_fields = True

    def active(qset):
        return qset.filter(is_active=True)


class Endpoint(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, unique=True, max_length=100)
    url = models.URLField()
    timeout = models.DurationField(default=datetime.timedelta(seconds=5))
    expected_status = models.SmallIntegerField()
    expected_text = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(db_index=True, default=True)
    is_up = models.BooleanField(db_index=True, default=True)
    group = models.ForeignKey(Group, related_name='endpoints')
    subscribers = models.ForeignKey(User, related_name='endpoints')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EndpointManager()

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
    def avg_response_time(self):
        try:
            return self.pings.passed().aggregate(
                Avg('response_time'))['response_time__avg']
        except:
            pass

    def __unicode__(self):
        return u"{name}".format(self.__dict__)

    def save(self, *args, **kwargs):
        self.ensure_slug()
        super(Endpoint, self).save(*args, **kwargs)

    def ensure_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)[:100].rstrip('-')


class PingManager(models.Manager):
    use_for_related_fields = True

    def passed(qset):
        return qset.filter(disposition=PASS)

    def failed(qset):
        return qset.filter(disposition__gt=PASS)


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

    def __unicode__(self):
        return u"{endpoint}: {disposition}@{created_at}".format(self.__dict__)
