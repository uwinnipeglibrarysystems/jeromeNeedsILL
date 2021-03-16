This project code uses Django (djangoproject.com), 3.2 series, currently in beta, but slated to be the next long term support (LTS) release.

The Django docs (https://docs.djangoproject.com/en/3.2/) cover what is involved in running a Django project.

To run this code for development, you'll need a python environment like a virtualenv with Django 3.2 (and other dependencies). Django 3.2 and its dependencies are in requirments.txt (output of pip freeze).

One dependency of this project is not availble through requirements.txt, pip and PyPY (Python Package Index). This is https://github.com/uwinnipeglibrarysystems/oclchmac .  You'll need to make that available for this Django app manually by ensuring the oclcwskeyhmacsig.util and oclcwskeyhmacsig.hmacsig libraries are available in the python path.

The Django settings file jeromeneedsill/settings.py imports a development SECRET_KEY from jeromeneedsill/secretkey.py, so you'll have to create that file. jeromeneedsill/secretkey_template.py includes an example or can be run
$ python jeromeneedsill/secretkey_template.py > jeromeneedsill/secretkey.py

Don't commit secretkey.py to revision control.

$ python ./manage.py migrate
will initialize your development database (sqllite)

# python ./manage.py runserver
runs a development web server.