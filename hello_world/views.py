# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from django.http import HttpResponse

from hello_world.versioning import is_api_version, versioned_method

def hello(request):
    return HttpResponse('hello world')

def timestamp(request):
    if is_api_version(request, '1'):
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    return HttpResponse(now.isoformat())

def utctimestamp(request):
    now = datetime.datetime.utcnow()
    return HttpResponse(now.isoformat())
