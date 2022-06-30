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

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache

from jeromeneedsill.nciplookupuser import (
    extract_user_identifier_from_ncip_lookup_user_XML,
    ncip_lookup_user_xml_response_element_tree_as_string,
    ncip_lookup_user_response_error_element_tree_as_string,
    )

TEST_USER_IDENT = '11111-11111'

def http_lookup_user_response_w_settings(
        privilege_profile, user_identifier, **kargs):
    kargs['language'] = settings.NCIP_LOOKUP_USER_LANGUAGE

    kargs['user_privileges'] = (
        {'AgencyId': settings.NCIP_LOOKUP_USER_PRIVILEGE_AGENCY_ID,
         'AgencyUserPrivilegeType': "STATUS",
         'privilege_type_scheme':
         settings.NCIP_LOOKUP_USER_PRIVILEGE_AUPT_SCHEME,
         'UserPrivilegeStatusType': "ACTIVE",
         'privilege_status_type_scheme':
         settings.NCIP_LOOKUP_USER_PRIVILEGE_UPST_SCHEME,
        },
        {'AgencyId': settings.NCIP_LOOKUP_USER_PRIVILEGE_AGENCY_ID,
         'AgencyUserPrivilegeType': "PROFILE",
         'privilege_type_scheme':
         settings.NCIP_LOOKUP_USER_PRIVILEGE_AUPT_SCHEME,
         'UserPrivilegeStatusType': privilege_profile,
         'privilege_status_type_scheme':
         settings.NCIP_LOOKUP_USER_PRIVILEGE_UPST_SCHEME,
        },
    )

    if 'barcode' in kargs:
        kargs['barcode_key_schema'] = \
        settings.NCIP_LOOKUP_USER_PRIMARY_KEY_IDENTIFIER_TYPE_SCHEME
        kargs['primary_key'] = kargs['barcode']
        kargs['primary_key_schema'] = kargs['barcode_key_schema']

    # agency, user_identifier,
    return HttpResponse(
        ncip_lookup_user_xml_response_element_tree_as_string(
            settings.NCIP_LOOKUP_USER_AGENCY, # agency
            user_identifier, # user_identifier
            **kargs),
        content_type="text/xml")

def http_lookup_user_response_unknown_user_error_w_settings():
    return HttpResponse(
        ncip_lookup_user_response_error_element_tree_as_string(
            settings.NCIP_LOOKUP_USER_AGENCY, # agency
            'Unknown User',
            'NCIP LookUpUser Processing Error Scheme'),
        content_type="text/xml")

@csrf_exempt
@require_POST
def ncip_lookup_user(request):
    user_ident = \
        extract_user_identifier_from_ncip_lookup_user_XML(request.body)
    # FIXME, we should also be looking at the request for
    # UserElementType: Name Information, User Address Information,
    # User Language, User Privilege, and User Id in the request and including
    # them in the response on that basis, not just automatically as is happening
    # below

    patron_profile = cache.get(user_ident)
    if patron_profile!=None: # if we found a UUID identified profile in cache
        # use a mapping configuration of OCLC borrowerCategory to
        # privilege_profile for the NCIP response, or fallback on a default
        # value settings.NCIP_LOOKUP_USER_DEFAULT_PRIVILEGE_PROFILE
        # if no catagory maps
        privilege_profile = \
            settings.NCIP_LOOKUP_USER_BORROWER_CAT_TO_PRIVILEGE_PROFILE_MAP.\
            get(patron_profile['borrowerCategory'],
                settings.NCIP_LOOKUP_USER_DEFAULT_PRIVILEGE_PROFILE)
        return http_lookup_user_response_w_settings(
            user_identifier=patron_profile['barcode'],
            barcode=patron_profile['barcode'],
            given_name=patron_profile['givenName'],
            surname=patron_profile['familyName'],
            email=patron_profile['email'],

            # FIXME, the privilege_profile should be be based on aspects of
            # patron type in the WMS response and probably the type mapping
            # should be defined in the django settings configuration
            privilege_profile=privilege_profile,
            )

    elif settings.DEBUG and user_ident == TEST_USER_IDENT:
        return http_lookup_user_response_w_settings(
            privilege_profile="Student",
            user_identifier=user_ident,
            given_name='Test',
            surname='User',
            email="test@localdomain",
            barcode="12345671234567",
        )
    elif ( hasattr(settings, 'NCIP_LOOKUP_USER_DEBUG_CACHE')
           and user_ident in settings.NCIP_LOOKUP_USER_DEBUG_CACHE ):
        # reminder, ** is the python operator for taking a dictionary and
        # using it as the basis to fill in arguments by name in a function
        # call
        return http_lookup_user_response_w_settings(
            **settings.NCIP_LOOKUP_USER_DEBUG_CACHE[user_ident] )
    else:
        return http_lookup_user_response_unknown_user_error_w_settings()
