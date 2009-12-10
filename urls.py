# copyright 2009 David Ignacio <deignacio@gmail.com>

from django.conf.urls.defaults import include, patterns

urlpatterns = patterns('',
                       (r'^v/(?P<api_version>\d+\.?\d*)/', include('hello_world.urls')),
                       ('', include('hello_world.urls')))
