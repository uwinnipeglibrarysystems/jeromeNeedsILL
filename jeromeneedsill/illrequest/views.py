from sys import stderr
from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.conf import settings

from .models import illrequestbase, openurlrequest

# FIXME this should really be loaded from a configurable django app, so other
# OAuth apis can be used other than oclc
#
# produces a url like
# https://oauth.oclc.org/auth/{registryID}?client_id={}&response_type=code&scope=SCIM:read_self
# client_id comes from settings.OCLC_SCIM_CLIENT_ID and needs to co-respond
# to the public identifier for a SCIM:read_self OCLC key
def construct_oclc_oauth_url(state=None, redirect_uri=None):
    """state and redirect_uri are optional, as None (defaults) they
    won't be included in the final url"""
    optional_state_component = (
        () if state==None # empty tuple
        else ( ('state', state), ) # single value tuple
        ) # end ternary expression

    optional_redirect_uri_component = (
        () if redirect_uri==None
        else ( ('redirect_uri', redirect_uri), ) # single value tuple
    ) # end ternary expression

    # tuple arithmatic here to add ( ('state', state), ) and
    # ('redirect_uri', redirect_uri) to the list of paramater pairs
    # passed to urlencode below
    return \
        settings.ILLREQUEST_OATH_URL + '?' + \
        urlencode( ( ('client_id', settings.ILLREQUEST_OCLC_SCIM_CLIENT_ID),
                     ('response_type', 'code'),
                     ('scope', 'SCIM:read_self') )
                   + # tuple arithmatic
                   optional_state_component + # tuple arithmatic
                   optional_redirect_uri_component )

# Create your views here.

def openurl_linkresolver(request):
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.GET
    else:
        raise Exception("request method other than GET/POST")

    # FIXME, instead of hard coding '/ill/requestlogin' there is django
    # way to identify this apps url by name, so the url can change
    # but the name stay the same
    url_encoded_ill_request = '/ill/requestlogin?' + urlencode( [
        (key, value)
        for key, value_list in params.lists()
        for value in value_list
            ] )

    return render(
        request, 'linkresolverfront.html',
        {'ill_request_url':url_encoded_ill_request} )

def openurl_requestlog_and_directtologin(request):
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.GET
    else:
        raise Exception("request method other than GET/POST")

    request_base = illrequestbase()
    request_base.save()
    for key, value_list in params.lists():
        for value in value_list:
            ourlr = openurlrequest(request=request_base, key=key, value=value)
            ourlr.save()

    return redirect(
        construct_oclc_oauth_url(
            state=str(request_base.id),
            redirect_uri=(
                None
                if not hasattr(settings,
                               'ILLREQUEST_POST_OAUTH_REDIRECT_URI')
                else settings.ILLREQUEST_POST_OAUTH_REDIRECT_URI
                ) # redirect_uri=
                ) ) # construct_oclc_oauth_url, redirect
