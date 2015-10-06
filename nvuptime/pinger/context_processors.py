from nvuptime.pinger.models import Outage


def outages(request):
    return {
        'current_outage': Outage.objects.active()[0],
        'recent_outage': Outage.objects.most_recent()
    }
