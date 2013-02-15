from django.conf.urls import patterns, include, url

urlpatterns = patterns('polls.models',
    url(r'^add/$', 'add'),
    url(r'^login/$', 'login'),
    url(r'^resetFixture/$', 'TESTAPI_resetFixture'),
    url(r'^unitTests/$', 'TESTAPI_unitTests'),
    
)