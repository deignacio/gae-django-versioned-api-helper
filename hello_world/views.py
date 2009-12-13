# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from django.http import HttpResponse
from django.utils import simplejson

from hello_world.versioning import get_api_version, is_api_version, versioned_method

def to_json(func):
    def inner_to_json(request, *args, **kwargs):
        obj = func(request, *args, **kwargs)
        json = simplejson.dumps(obj)
        return json
    return inner_to_json

def to_http_response(response_type=None):
    if response_type is None:
        response_type = HttpResponse
    def inner_return_to_http_response(func):
        def actual_return_to_http_response(request, *args, **kwargs):
            val = func(request, *args, **kwargs)
            return response_type(val)
        return actual_return_to_http_response
    return inner_return_to_http_response

@to_http_response()
def hello(request):
    return 'hello world'

@to_http_response()
def utctimestamp(request):
    now = datetime.datetime.utcnow()
    return now.isoformat()

@to_http_response()
@to_json
def utctimestamp_json(request):
    now = datetime.datetime.utcnow()
    data = { "now": now.isoformat() }
    return data

@versioned_method(versions={ '1':utctimestamp,
                             '2':utctimestamp_json })
@to_http_response()
def timestamp(request):
    now = datetime.datetime.now()
    return now.isoformat()

@to_http_response()
def version(request):
    return get_api_version(request)
