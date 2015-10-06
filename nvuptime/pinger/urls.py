"""nvuptime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from nvuptime.pinger import views

urlpatterns = [
    url(r'^groups/(?P<slug>[-a-z0-9]+)/$', views.GroupDetail.as_view(),
        name='group'),
    url(r'^endpoints/(?P<slug>[-a-z0-9]+)/$', views.EndpointDetail.as_view(),
        name='endpoint'),
    url(r'^pings/(?P<pk>[0-9]+)/$', views.PingDetail.as_view(),
        name='ping'),
    url(r'^outages/(?P<pk>[0-9]+)/$', views.OutageDetail.as_view(),
        name='outage'),
    url(r'^$', views.GroupDetail.as_view(), {'slug': 'public'}, name='public'),
]
