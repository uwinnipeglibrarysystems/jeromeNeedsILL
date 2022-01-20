#!/usr/bin/env python3

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
