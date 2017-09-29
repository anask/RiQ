from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', 'video.views.video'),
        url(r'^video$', 'video.views.video'),
)
