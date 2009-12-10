# mostly boilerplate code taken from
# http://code.google.com/appengine/articles/django.html

import os

ROOT_URLCONF = 'urls'

MIDDLEWARE_CLASSES = (
)

INSTALLED_APPS = (
    'hello_world'
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)
