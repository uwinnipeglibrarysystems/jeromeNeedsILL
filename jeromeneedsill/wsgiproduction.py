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
