# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from django.http import HttpResponse
from django.utils import simplejson

from hello_world.versioning import get_api_version, is_api_version, versioned_method

def hello(request):
    return HttpResponse('hello world')

def utctimestamp(request):
    now = datetime.datetime.utcnow()
    if is_api_version(request, '2'):
        data = { "now": now.isoformat() }
        json = simplejson.dumps(data)
        return HttpResponse(json)
    else:
        return HttpResponse(now.isoformat())

@versioned_method(versions={ '1':utctimestamp })
def timestamp(request):
    now = datetime.datetime.now()
    return HttpResponse(now.isoformat())

def version(request):
    return HttpResponse(get_api_version(request))
