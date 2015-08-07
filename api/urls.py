# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'checklist/$', 'api.views.checklist_list'),
    url(r'checklist/(?P<list_id>\w+)/$', 'api.views.checklist'),
    url(r'group/$', 'api.views.group_list'),
    url(r'group/(?P<group_id>\w+)/$', 'api.views.group'),
    url(r'invited_group/$', 'api.views.invited_group_list'),
)
