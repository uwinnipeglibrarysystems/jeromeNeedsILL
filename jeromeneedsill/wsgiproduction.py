# Copyright (c) 2021 University of Winnipeg
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
WSGI config for jeromeneedsill project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

DJANGO_TARGET_VARS = (
    'DJANGO_SECRET_KEY',
    'DJANGO_SECRET_MYSQL_PASSWORD',
    'ILLREQUEST_OCLC_SCIM_SECRET',
    'RELAIS_AUTH_API_KEY_SECRET',
    )

# our regards to
# https://stackoverflow.com/questions/19754834/access-apache-setenv-variable-from-django-wsgi-py-file

app_cache = None

def application(env, start):
    global app_cache
    if None == app_cache:
        for target_var in DJANGO_TARGET_VARS:
            if target_var in env:
                os.environ.setdefault(target_var, env[target_var])
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'jeromeneedsill.settings')
        app_cache = get_wsgi_application()
    return app_cache(env, start)
