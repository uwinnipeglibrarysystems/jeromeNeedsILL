[Jerome](https://en.wikipedia.org/wiki/Jerome) is considered the [patron saint](https://www.luther.edu/library/about/history/40th/jerome/) of librarians.

Perhaps he would have valued interlibrary loans as we do.

This is a web application which:
 1) Captures an incoming OpenURL request representing an ILL request to a database
 2) Asks the user if they would like to place an ill request
 3) Authenticates the user against OCLC OAuth api
 4) Fetches a user profile with OCLC SCIM /Me API and stores name, email and barcode in the database connected to the ILL request
 5) Optionally sends the user to Relais Portal to place their ILL request there, a process which involves: i) requesting an authentication id (aid), ii) potentially providing the patron profile to Relais through the NCIP Lookup User operation, iii) redirecting the patron to Relais Portal with the aid

Code here was developed by staff of the systems team at the University of Winnipeg Library. Free software licensing is pending.

This application is in early release. It's not even in production yet at the University of Winnipeg where it was developed. Minimal viable product status was only achieved in March 2021 (tag mvp0.1).

Note that production deployment instructions are not included at this time. Like all Django apps, if you are going to deploy to production, cryptographic secrets should not be found in source code files and should be passed on to settings.py by way of environment variables that the production web server passes on.

Releases will be tagged.

This project code uses [Django](https://djangoproject.com), 3.2 series, the current long term support (LTS) release.

The [Django docs](https://docs.djangoproject.com/en/3.2/) cover what is involved in running a Django project.

To run this code for development, you'll need Python 3.6 or later, a Django 3.2.x installation, [python-requests](https://docs.python-requests.org/) and their dependencies.

You may find it convient to use the [python venv module](https://docs.python.org/3/library/venv.html) to contain these dependencies instead of installing them system wide. A venv will also typically include the pip3 too.

Django 3.2 and python-requests are specified in the requirements.txt file. You can install both of those requirements and their dependencies with
$ pip3 install -r requirements.txt

One dependency of this project is not availble through requirements.txt, pip and PyPY (Python Package Index). This is [oclchmac](https://github.com/uwinnipeglibrarysystems/oclchmac) .  You'll need to make that available for this Django app manually by ensuring the oclcwskeyhmacsig.util and oclcwskeyhmacsig.hmacsig libraries are available in the python path.

The Django settings file jeromeneedsill/settings.py imports a development SECRET_KEY from jeromeneedsill/secretkey.py, so you'll have to create that file. jeromeneedsill/secretkey_template.py includes an example or can be run
$ python3 jeromeneedsill/secretkey_template.py > jeromeneedsill/secretkey.py

You'll also need an OCLC SCIM API key with access to the /Me endpoint and circulation info. Establish a jeromeneedsill/sitesettings.py file with at least ILLREQUEST_OCLC_SCIM_CLIENT_ID and ILLREQUEST_OCLC_SCIM_SECRET if you are using a development API key that uses the OCLC test institution and define ILLREQUEST_INSTITUTION_ID as well if you are using a production API key with your institution.

Note, in deployment ILLREQUEST_OCLC_SCIM_SECRET should not be in a file at all but passed to to a customized settings.py by way of environment variables set by a web server.

Don't commit secretkey.py and to revision control or sitesettings.py if it contains ILLREQUEST_OCLC_SCIM_SECRET .

There are many settings possible through settings.py or sitesettings.py . Many are listed in jeromeneedsill/sitesettings.py.example and jeromeneedsill/sitesettings.py.production.example, though more documentation is still called for.

Once you have a satisfactory configuration in secretkey.py, settings.py and sitesetting.py, you can run:

`$ ./manage.py migrate`

to initialize your development database (sqllite)

`$ ./manage.py createcachetable`

will create tables in your database for caching OCLC WMS profiles. In production
you might want to use a different caching behavior by overriding CACHES in sitesettings.py .

`$ ./manage.py runserver`

runs a development web server.
