#!/usr/bin/env python3

# For your development, create a secretkey.py with a SECRET_KEY='' line like
# the following:

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='django-insecure'

# Or run this file
# python secret_keytemplate.py > secretkey.py
# to get a file with a random SECRET_KEY= string
#
# for production needs, setting.py should do something like use a envirionmental
# variable to import SECRET_KEY
# Don't commit a SECRET_KEY to revision control

if __name__ == "__main__":
    from django.core.management.utils import get_random_secret_key
    print("SECRET_KEY='django-insecure" + get_random_secret_key() + "'")
