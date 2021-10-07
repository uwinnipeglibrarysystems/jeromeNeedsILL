#!/usr/bin/env python3

import cgi

# only for debugging in development
#import cgitb
#cgitb.enable()

from sys import stdout
import os
from urllib.parse import urlencode

# configure this
REDIR_DEST='http://localhost:9001/ill/requestloginwiplog'

form = cgi.FieldStorage()

def http_print_lineend():
    stdout.write("\r\n")
    stdout.flush()

def http_print(line):
    stdout.write(line)
    http_print_lineend()

http_print("Status: 302 Found")
http_print("Location: " + REDIR_DEST + "?" +
           urlencode( (
               ("state", form.getfirst("state", "none")),
           ("ip", os.environ['REMOTE_ADDR']) ) ) )
http_print_lineend()
