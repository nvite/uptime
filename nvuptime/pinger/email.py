import threading

from collections import Counter

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
# from django.utils import timezone


class BasePostmarkEndpointEmailThread(threading.Thread):
    def __init__(self, endpoint, **kwargs):
        super(BasePostmarkEndpointEmailThread, self).__init__(**kwargs)
        self.endpoint = endpoint
        self.ping = endpoint.pings.first()
        self.sender = settings.POSTMARK_SENDER
        self.recipients = [user.email for user
                           in self.endpoint.subscribers.all()]
        self.data = self.ping.__dict__
        self.data['endpoint'] = self.endpoint.__str__()
        self.data['disposition'] = self.ping.get_disposition_display()
        self.data['timestamp'] = self.ping.created_at

    @property
    def should_send(self):
        # feel free to spam admins whenever, but nobody else.
        admins = Counter(dict(settings.ADMINS).values())
        recipients = Counter(self.recipients)
        should_send = not (settings.DEBUG is True and
                           len(list(recipients - admins)) is not 0)
        return should_send

    def run(self):
        headers = {}
        try:
            headers = self.headers
        except AttributeError:
            pass
        if self.should_send:
            msg = EmailMultiAlternatives(self.subject, self.text_body, self.sender,
                                         self.recipients, headers=headers)
            msg.attach_alternative(self.html_body, "text/html")
            msg.send()
        else:
            print("Suppressing email because reasons. %s" % self.subject)


class EndpointDownEmailThread(BasePostmarkEndpointEmailThread):
    def __init__(self, endpoint, **kwargs):
        super(EndpointDownEmailThread, self).__init__(endpoint, **kwargs)
        self.headers = {'Reply-To': 'nerds@nvite.com', }
        self.subject = '[nvite monitoring] Ping failed for {endpoint}'.format(**self.data)
        self.text_body = render_to_string("pinger/emails/down.txt", context=self.data)
        self.html_body = render_to_string("pinger/emails/down.html", context=self.data)


class EndpointUpEmailThread(BasePostmarkEndpointEmailThread):
    def __init__(self, endpoint, **kwargs):
        super(EndpointUpEmailThread, self).__init__(endpoint, **kwargs)
        self.headers = {'Reply-To': 'nerds@nvite.com', }
        self.subject = '[nvite monitoring] Ping succeeded for {endpoint}'.format(**self.data)
        self.text_body = render_to_string("pinger/emails/up.txt", context=self.data)
        self.html_body = render_to_string("pinger/emails/up.html", context=self.data)
