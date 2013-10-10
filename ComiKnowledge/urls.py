# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ck.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', 'ck.views.home'),
    url(r'^login/$', 'ck.views.login'),
    url(r'^logout/$', 'ck.views.logout'),
    url(r'', include('social_auth.urls')),
    # url(r'^ComiKnowledge/', include('ComiKnowledge.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
