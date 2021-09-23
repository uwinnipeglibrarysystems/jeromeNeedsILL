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
        return http_lookup_user_response_w_settings(
            user_identifier=patron_profile['barcode'],
            barcode=patron_profile['barcode'],
            given_name=patron_profile['givenName'],
            surname=patron_profile['familyName'],
            email=patron_profile['email'],

            # FIXME, the privilege_profile should be be based on aspects of
            # patron type in the WMS response and probably the type mapping
            # should be defined in the django settings configuration
            privilege_profile="Student",
            )

    elif user_ident == TEST_USER_IDENT:
        return http_lookup_user_response_w_settings(
            privilege_profile="Student",
            user_identifier=user_ident,
            given_name='Test',
            surname='User',
            email="test@localdomain",
            barcode="12345671234567",
        )
    else:
        return http_lookup_user_response_unknown_user_error_w_settings()
