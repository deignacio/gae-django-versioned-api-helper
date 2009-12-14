# mostly boilerplate code taken from
# http://code.google.com/appengine/articles/django.html

import os

ROOT_URLCONF = 'urls'

DEBUG = True

MIDDLEWARE_CLASSES = (
    'hello_world.versioning.ApiVersionMiddleware',
)

INSTALLED_APPS = (
    'hello_world'
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)
