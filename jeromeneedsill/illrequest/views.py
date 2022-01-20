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

from sys import stderr
from urllib.parse import urlencode
from ipaddress import ip_address

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from jeromeneedsill.ipmatchrules import get_rule_if_ip_matches

from .models import \
    illrequestbase, openurlrequest, illrequestdiscoveredipaddress

from .postoauth import post_oauth
from .genrefix import param_list_has_genre_problem, ask_for_genre_problem_fix
from .util import get_client_ip_addr_from_request

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

def create_django_redirect_to_oclc_oauth_for_request_state_uuid(request_uuid):
    return redirect(
        construct_oclc_oauth_url(
            state=request_uuid,
            redirect_uri=(
                None
                if not hasattr(settings,
                               'ILLREQUEST_POST_OAUTH_REDIRECT_URI')
                else settings.ILLREQUEST_POST_OAUTH_REDIRECT_URI
                ) # redirect_uri=
                ) ) # construct_oclc_oauth_url, redirect

# Create your views here.

@csrf_exempt
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
    target_url = '/ill/requestlogin'
    paramlist = [
        (key, value)
        for key, value_list in params.lists()
        for value in value_list
    ]

    if param_list_has_genre_problem(paramlist):
        return ask_for_genre_problem_fix(request, target_url, paramlist)
    else:
        url_encoded_ill_request = target_url + '?' + urlencode(paramlist)
        return render(
            request, 'linkresolverfront.html',
            {'ill_request_url':url_encoded_ill_request} )

def openurl_requestlog_and_directtologin(request):
    # shortcut, if the request state has already been saved before
    # then load it
    if request.method == 'GET' and 'state' in request.GET:
        try:
            request_base = illrequestbase.objects.get(id=request.GET['state'])
        # I don't expect to see this
        except illrequestbase.DoesNotExist:
            raise Exception("non-matching ill request state")

    # otherwise, default behavior of inspecting the request state for
    # problems and saving it
    #
    # either way, outcome is request_base assigned a illrequestbase object
    else:
        if request.method == 'POST':
            params = request.POST
        elif request.method == 'GET':
            params = request.GET
        else:
            raise Exception("request method other than GET/POST")

        paramlist = [
            (key, value)
            for key, value_list in params.lists()
            for value in value_list
        ]

        # check if the user had been sent to genrefix.html and didn't
        # select a new item genre
        #
        # if so, send them back
        if param_list_has_genre_problem(paramlist):
            # FIXME, instead of hard coding '/linkresolver' there is django
            # way to identify this apps url by name, so the url can change
            # but the name stay the same
            linkresolver_url = '/linkresolver'
            return redirect(
                linkresolver_url + '?' + urlencode(paramlist)
                )

        request_base = illrequestbase()
        request_base.save()
        for key, value in paramlist:
            ourlr = openurlrequest(request=request_base, key=key, value=value)
            ourlr.save()

    request_uuid = str(request_base.id)

    if hasattr(settings, 'ILLREQUEST_IP_CORRECTION_RANGES'):
        matching_rule = get_rule_if_ip_matches(
            get_client_ip_addr_from_request(request),
            settings.ILLREQUEST_IP_CORRECTION_RANGES)
        if matching_rule and matching_rule.startswith('http'):
            return redirect(
                matching_rule + '?' +
                urlencode( ( ('state', request_uuid), ) ) )
        elif matching_rule: # otherwise an ip string
            # if the rules provided an ip string, we just validate it,
            # log it, and proceed normally with oclc oauth_login
            try:
                ip_address(matching_rule)
            except ValueError:
                raise Exception(
                    "invalid ip address target %s in "
                    "setttings.ILLREQUEST_IP_CORRECTION_RANGES" % matching_rule)
            illrdip = illrequestdiscoveredipaddress(
                request=request_base,
                original_ip=get_client_ip_addr_from_request(request),
                outside_ip=matching_rule)
            illrdip.save()
            # could have also left this out and relied on fall-through
            return create_django_redirect_to_oclc_oauth_for_request_state_uuid(
                request_uuid)
        # if matching_rule is False, that means no rule matches
        # in which case none of the rules are required and we fall through
        # below to the default behavior of just sending the patron to
        # OCLC oauth
        else:
            pass

    return create_django_redirect_to_oclc_oauth_for_request_state_uuid(
        request_uuid)

@csrf_exempt
def log_ip_and_directtologin(request):
    if request.method != 'GET':
        raise Exception("expected method is GET")
    if not ('state' in request.GET and 'ip' in request.GET):
        raise Exception("state and ip paramaters are required")

    request_uuid = request.GET['state']
    try:
        illrbase = illrequestbase.objects.get(id=request_uuid)
    # I don't expect to see this
    except illrequestbase.DoesNotExist:
        raise Exception("non-matching ill request state")

    # FIXME, add validation of request.GET['ip'] as being well-formed
    illrdip = illrequestdiscoveredipaddress(
        request=illrbase,
        original_ip=get_client_ip_addr_from_request(request),
        outside_ip=request.GET['ip'])
    illrdip.save()

    return create_django_redirect_to_oclc_oauth_for_request_state_uuid(
        request_uuid)
