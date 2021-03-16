This project code uses Django (djangoproject.com), 3.2 series, currently in beta, but slated to be the next long term support (LTS) release.

The Django docs (https://docs.djangoproject.com/en/3.2/) cover what is involved in running a Django project.

To run this code for development, you'll need a python environment like a virtualenv with Django 3.2 (and other dependencies). Full dependencies are in requirments.txt (output of pip freeze).

The Django settings file jeromeneedsill/settings.py imports a development SECRET_KEY from jeromeneedsill/secretkey.py, so you'll have to create that file. jeromeneedsill/secretkey_template.py includes an example or can be run
$ python jeromeneedsill/secretkey_template.py > jeromeneedsill/secretkey.py

Don't commit secretkey.py to revision control.

$ python ./manage.py migrate
will initialize your development database (sqllite)

# python ./manage.py runserver
runs a development web server.