from django.views.generic.detail import DetailView
# from django.views.generic.list import ListView

from nvuptime.pinger.models import Group, Endpoint, Ping


class GroupDetail(DetailView):
    http_method_names = ['head', 'get', 'options']
    template_name = 'pinger/group.html'
    model = Group


class EndpointDetail(DetailView):
    http_method_names = ['head', 'get', 'options']
    template_name = 'pinger/endpoint.html'
    model = Endpoint

    def get_context_data(self, **kwargs):
        ctx = super(EndpointDetail, self).get_context_data(**kwargs)
        ctx['latest_pings'] = ctx['object'].pings.all().order_by('-created_at')[:15]
        return ctx


class PingDetail(DetailView):
    http_method_names = ['head', 'get', 'options']
    template_name = 'pinger/ping.html'
    model = Ping
