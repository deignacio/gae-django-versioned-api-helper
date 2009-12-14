# copyright 2009 David Ignacio <deignacio@gmail.com>

from django.http import HttpResponse
from django.utils import simplejson

def to_json(func):
    def inner_to_json(request, *args, **kwargs):
        obj = func(request, *args, **kwargs)
        json = simplejson.dumps(obj)
        return json
    return inner_to_json

def to_http_response(response_type=None):
    if response_type is None:
        response_type = HttpResponse
    def inner_to_http_response(func):
        def actual_to_http_response(request, *args, **kwargs):
            val = func(request, *args, **kwargs)
            return response_type(val)
        return actual_to_http_response
    return inner_to_http_response

