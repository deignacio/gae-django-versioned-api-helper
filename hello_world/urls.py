# copyright 2009 David Ignacio <deignacio@gmail.com>

from django.conf.urls.defaults import include, patterns

urlpatterns = patterns('hello_world.views',
                       (r'timestamp', 'timestamp'),
                       (r'utctimestamp', 'utctimestamp'),
                       (r'version', 'version'),
                       (r'', 'hello'))
