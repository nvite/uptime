from __future__ import absolute_import
import datetime
import re

from celery import shared_task
import requests

from nvuptime.pinger.models import (Endpoint, Ping,
                                    PASS, TIMEOUT, MISMATCH, ERROR)


@shared_task
def ping_endpoints():
    for endpoint in Endpoint.objects.active():
        endpoint.is_up = False

        data = {
            'endpoint': endpoint,
        }

        start = datetime.datetime.now()
        try:
            res = requests.get(endpoint.url, timeout=endpoint.timeout.seconds)
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
