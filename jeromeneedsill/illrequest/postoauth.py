from urllib.parse import urlencode
from django.shortcuts import render

from jeromeneedsill.oclcwmsapis import (
    OCLCApiFail,
    get_oclc_access_token,
    get_oclc_wms_simplified_patron_profile,
    )

from .models import illrequestbase, openurlrequest, illmanualrequester

def oauth_error_w_known_state(request, illrbase):
    return render(
        request, 'error_with_known_state.html',
        {'illrequestbase': illrbase,
         'illopenurlparams': openurlrequest.objects.filter(request=illrbase) })

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

        requester = illmanualrequester(
            request=illrbase,
            requester_name=patron_profile['name'],
            email=patron_profile['email'],
            barcode=patron_profile['barcode'] )
        requester.save()

        return render(
            request, 'ill_success_with_patron_details.html',
            {'patron_profile': patron_profile} )
