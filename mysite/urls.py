from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^users/', include('polls.urls')),
    url(r'^TESTAPI/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
)