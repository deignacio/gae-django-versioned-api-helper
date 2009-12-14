# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from hello_world.decorators import to_http_response, to_json
from hello_world.versioning import get_api_version, is_api_version, versioned_method

@to_http_response()
def hello(request):
    return 'hello world'

def utctimestamp(request):
    now = datetime.datetime.utcnow()
    return now.isoformat()

@to_json
def utctimestamp_json(request):
    now = datetime.datetime.utcnow()
    data = { "now": now.isoformat() }
    return data

@to_http_response()
@versioned_method(versions={ '1':utctimestamp,
                             '2':utctimestamp_json })
def timestamp(request):
    now = datetime.datetime.now()
    return now.isoformat()

@to_http_response()
def version(request):
    return get_api_version(request)
