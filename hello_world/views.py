# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from hello_world.decorators import to_http_response, to_json
from hello_world.versioning import build_registered_version_handler, get_api_version, is_api_version, register_version, versioned_method

@to_http_response()
def hello(request):
    return 'hello world'


@register_version("timestamp", "1")
@to_http_response()
def utctimestamp(request):
    now = datetime.datetime.utcnow()
    return now.isoformat()

@register_version("timestamp", "2")
@to_http_response()
@to_json
def utctimestamp_json(request):
    now = datetime.datetime.utcnow()
    data = { "now": now.isoformat() }
    return data

@register_version("timestamp", "0")
@to_http_response()
def original_timestamp(request):
    now = datetime.datetime.now()
    return now.isoformat()

timestamp = build_registered_version_handler("timestamp")

@to_http_response()
def version(request):
    return get_api_version(request)
