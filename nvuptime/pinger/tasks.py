from __future__ import absolute_import
import datetime
import re
import threading

from celery import shared_task
import requests

from django.conf import settings

from nvuptime.pinger.models import (Group, Ping, Outage,
                                    PASS, TIMEOUT, MISMATCH, ERROR)


class GroupPingerThread(threading.Thread):
    def __init__(self, group, **kwargs):
        self.group = group
        self.endpoints = []
        if group.is_active:
            self.endpoints = group.endpoints.active()

    def run(self):
        for endpoint in self.endpoints:
            if not endpoint.is_due:
                continue

            endpoint.is_up = False

            data = {
                'endpoint': endpoint,
            }

            start = datetime.datetime.now()
            try:
                res = requests.get(endpoint.url,
                                   timeout=endpoint.timeout.seconds)
            except requests.exceptions.Timeout as e:
                data['disposition'] = TIMEOUT
                data['response'] = e
            except requests.exceptions.RequestException as e:
                data['disposition'] = ERROR
                data['response'] = e
            end = datetime.datetime.now()

            data['response_time'] = (end - start).total_seconds()
            data['response_code'] = res.status_code
            data['response_headers'] = res.headers

            if 'response' not in data.keys():
                data['response'] = res.text

            if ('disposition' not in data.keys() and
                res.status_code is endpoint.expected_status and
                (not endpoint.expected_text or
                    re.search(re.escape(endpoint.expected_text),
                              res.text, re.IGNORECASE))):
                data['disposition'] = PASS
                endpoint.is_up = True
                # let's delete our headers and body when things look good
                # to save db space
                del data['response']
                del data['response_headers']

            else:
                data['disposition'] = MISMATCH

            ping = Ping(**data)
            ping.save()
            endpoint.save()

            # If an endpoint in the public group has been down for n times
            # we should automatically create an 'outage' event
            if (endpoint.is_up is False and
                endpoint.group.slug is 'public' and
                len([ping for ping in endpoint.pings.all()[0, settings.OUTAGE_THRESHOLD]
                          if ping.disposition == PASS]) is 0):
                Outage.objects.get_or_create(end=None)


@shared_task
def ping_endpoints():
    for group in Group.objects.active():
        GroupPingerThread(group).run()
