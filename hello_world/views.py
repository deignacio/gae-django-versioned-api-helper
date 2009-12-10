# copyright 2009 David Ignacio <deignacio@gmail.com>

from django.http import HttpResponse

def hello(request):
    return HttpResponse('hello world')
