Jerome is considered the patron saint of librarians.
https://en.wikipedia.org/wiki/Jerome
https://www.luther.edu/library/about/history/40th/jerome/

Perhaps he would have valued interlibrary loans as we do.

This is a web application which:
 1) Captures an incoming OpenURL request representing an ILL request to a database
 2) Asks the user if they would like to place an ill request
 3) Authenticates the user against OCLC OAuth api
 4) Fetches a user profile with OCLC SCIM /Me API and stores name, email and barcode in the database connected to the ILL request

Code here was developed by staff of the systems team at the University of Winnipeg Library. Free software licensing is pending.

This application is in early release. It's not even in production yet at the University of Winnipeg where it was developed. Minimal viable product status was only achieved in March 2021.

Releases will be tagged.

Planned is support for Relais APIs so that user profiles and ILL requests can land there for direct handling by ILL staff and only pass through this Django web app.

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