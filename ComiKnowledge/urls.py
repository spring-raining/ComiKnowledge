# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ck.views.index'),
    url(r'^home/$', 'ck.views.home'),
    url(r'^login/$', 'ck.views.login'),
    url(r'^logout/$', 'ck.views.logout'),
    url(r'^checklist/$', 'ck.views.checklist'),
    url(r'^checklist/(?P<list_id>\d+)/$', 'ck.views.checklist_edit'),
    url(r'^group/$', 'ck.views.group'),
    url(r'^group/(?P<group_id>\w+)/$', 'ck.views.group_home'),
    url(r'', include('social_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
