# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ck.views.index'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^home/$', 'ck.views.home'),
    url(r'^login/$', 'ck.views.login'),
    url(r'^logout/$', 'ck.views.logout'),
    url(r'^checklist/$', 'ck.views.checklist'),
    url(r'^checklist/(?P<list_id>\w+)/$', 'ck.views.checklist_edit'),
    url(r'^checklist/(?P<list_id>\w+)/download$', 'ck.views.checklist_download'),
    url(r'^group/$', 'ck.views.group'),
    url(r'^group/(?P<group_id>\w+)/$', 'ck.views.group_home'),
    url(r'^group/(?P<group_id>\w+)/create$', 'ck.views.group_checklist_create'),
    url(r'', include('social_auth.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
