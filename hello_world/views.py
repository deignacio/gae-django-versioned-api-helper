# copyright 2009 David Ignacio <deignacio@gmail.com>

import datetime

from django.http import HttpResponse

def hello(request):
    return HttpResponse('hello world')

def timestamp(request):
    now = datetime.datetime.now()
    return HttpResponse(now.isoformat())
