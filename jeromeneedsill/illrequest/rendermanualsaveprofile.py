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

from django.shortcuts import render

from .models import openurlrequest, illmanualrequester

# FIXME, this should really have an error paramater for situations where
# we're calling this because of an error trying to avoid a manual entry
# vs situations where this is done because the configuration doesn't
# establish that automatic injection into something like Relais
#
# an error could be displayed to users in those cases to let them know
# their request may take a bit more to process
#
# and additional handling can occur in the error cases such as staff
# notification
def render_post_oauth_manual_save_profile(
        request, illrbase, patron_profile, error=None):
    requester = illmanualrequester(
        request=illrbase,
        requester_name=patron_profile['name'],
        email=patron_profile['email'],
        barcode=patron_profile['barcode'] )
    requester.save()

    params = openurlrequest.objects.filter(request=illrbase)

    return render(
        request, 'ill_success_with_patron_details.html',
        {'patron_profile': patron_profile,
         'error': error,
         'params': params,
        } )
