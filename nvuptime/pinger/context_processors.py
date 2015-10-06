from nvuptime.pinger.models import Outage


def outages(request):
    current_outage = None
    most_recent_outage = None
    if Outage.objects.already_down():
        current_outage = Outage.objects.active()[0]
        recent_outage = Outage.objects.most_recent()
        return {
            'current_outage': current_outage,
            'recent_outage': recent_outage
        }
