from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'execute.views.land'),
	url(r'^getquery/$', 'execute.views.getQueryList'),
)
