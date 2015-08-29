import threading

from collections import Counter

from django.core.mail import EmailMessage
from django.conf import settings
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
        return not (settings.DEBUG is True and
                    len(list(recipients - admins)) is not 0)

    def run(self):
        headers = {}
        try:
            headers = self.headers
        except AttributeError:
            pass
        if self.should_send:
            EmailMessage(self.subject, self.body, self.sender, self.recipients,
                         headers=headers).send()
        else:
            print("Suppressing email because reasons. %s" % self.subject)


class EndpointDownEmailThread(BasePostmarkEndpointEmailThread):
    def __init__(self, endpoint, **kwargs):
        super(EndpointDownEmailThread, self).__init__(endpoint, **kwargs)
        self.headers = {'Reply-To': 'nerds@nvite.com', }
        self.subject = '[nvite monitoring] Ping failed for {endpoint}'.format(**self.data)
        self.body = ("We are writing to let you know that your endpoint, {endpoint} "
                     "is down as of {timestamp}. The details:"
                     "\n\n"
                     "Disposition: {disposition}\n"
                     "Status Code: {response_code}\n"
                     "Response Time: {response_time}\n"
                     "Response (if any):\n"
                     "{response}").format(**self.data)


class EndpointUpEmailThread(BasePostmarkEndpointEmailThread):
    def __init__(self, endpoint, **kwargs):
        super(EndpointUpEmailThread, self).__init__(endpoint, **kwargs)
        self.headers = {'Reply-To': 'nerds@nvite.com', }
        self.subject = '[nvite monitoring] Ping succeeded for {endpoint}'.format(**self.data)
        self.body = ("Good news! your endpoint, {endpoint} is back up as "
                     "of {timestamp}. The details:"
                     "\n\n"
                     "Disposition: {disposition}\n"
                     "Status Code {response_code}\n"
                     "Response Time: {response_time}\n").format(**self.data)
