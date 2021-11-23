from urllib.parse import urlencode
from uuid import uuid4

from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings

from jeromeneedsill.oclcwmsapis import (
    OCLCApiFail,
    get_oclc_access_token,
    get_oclc_wms_simplified_patron_profile,
    )

from .relaisill import refer_profile_and_request_to_relais
from .rendermanualsaveprofile import render_post_oauth_manual_save_profile

from .models import illrequestbase, openurlrequest, illmanualrequester

def oauth_error_w_known_state(request, illrbase):
    return render(
        request, 'error_with_known_state.html',
        {'illrequestbase': illrbase,
         'illopenurlparams': openurlrequest.objects.filter(request=illrbase) })

def ncip_cached_profile_setting_w_uuid():
    return (
        hasattr(settings,'RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_UUID')
        and
        settings.RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_UUID)

def ncip_cached_profile_setting_w_barcode():
    return (
      hasattr(settings,'RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_BARCODE')
      and
      settings.RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_BARCODE)

def ncip_cached_profile_setting_in_use():
    cached_profile_uuid = ncip_cached_profile_setting_w_uuid()
    cached_profile_barcode = ncip_cached_profile_setting_w_barcode()
    return ( (cached_profile_uuid or cached_profile_barcode) and
             not settings.RELAIS_REQUEST_RELAID_AID_W_BARCODE)

def post_oauth(request):
    if 'state' in request.GET:
        try:
            illrbase = illrequestbase.objects.get(id=request.GET['state'])
        # I don't expect to see this
        except illrequestbase.DoesNotExist:
            raise Exception("non-matching ill request state")

    if 'error' in request.GET and 'state' in request.GET:
        return oauth_error_w_known_state(request, illrbase)
    elif 'error' in request.GET: # but not 'state' in request.GET
        return render(
            request, 'error_without_save.html',
            {'error': request.GET['error'],
             'error_description': request.GET.get('error_description', '') } )
    elif 'code' not in request.GET:
        raise Exception(
            "did not expect OCLC redirect to end with no error or no code")
    elif 'state' not in request.GET:
        # I don't really expect to see this, so not directing to an
        # elegant handler
        raise Exception("successful login didn't come with state")
    else: # else we got a code and state, use them
        try:
            access_token = get_oclc_access_token(request.GET['code'])
        except OCLCApiFail as e:
            return oauth_error_w_known_state(request, illrbase)

        try:
            patron_profile = get_oclc_wms_simplified_patron_profile(
                access_token)
        except OCLCApiFail as e:
            return oauth_error_w_known_state(request, illrbase)

        if ( hasattr(settings, 'RELAIS_REFER_PROFILE_AND_REQUEST_TO_RELAIS')
             and
             settings.RELAIS_REFER_PROFILE_AND_REQUEST_TO_RELAIS ):

            # if we're caching the patron profile so as to respond to
            # /nciplookupuser/ after providing relais with a random UUID
            if ncip_cached_profile_setting_in_use():
                # cache the patron profile with a random (type 4) UUID
                # so it can be retrieved by Relais calling /nciplookupuser/
                if ncip_cached_profile_setting_w_uuid():
                    profile_ident = str(uuid4())
                elif ncip_cached_profile_setting_w_barcode():
                    profile_ident = patron_profile['barcode']
                else: # one of the above will always apply
                    assert(False)
                cache.set(profile_ident, patron_profile)

                return refer_profile_and_request_to_relais(
                    request, profile_ident, illrbase, patron_profile)

            # of, if we're providing Relais a bacode because we are having it
            # ask some other NCIP server or rely on profiles already there
            elif (hasattr(settings, 'RELAIS_REQUEST_RELAID_AID_W_BARCODE')
                  and settings.RELAIS_REQUEST_RELAID_AID_W_BARCODE and
                  not settings.RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_UUID
            ):
                return refer_profile_and_request_to_relais(
                    request, patron_profile['barcode'],
                    illrbase, patron_profile)
            else:
                raise Exception(
                    "settings misconfiguration, one and only one of "
                    "RELAIS_REQUEST_RELAIS_AID_W_CACHED_PROFILE_UUID "
                    "and RELAIS_REQUEST_RELAID_AID_W_BARCODE must be set "
                    "when RELAIS_REFER_PROFILE_AND_REQUEST_TO_RELAIS is enabled"
                    )
        else:
            return render_post_oauth_manual_save_profile(
                request, illrbase, patron_profile)
