# copyright 2009 David Ignacio <deignacio@gmail.com>

from django.conf.urls.defaults import include, patterns

urlpatterns = patterns('',
                       ('', include('hello_world.urls')))
