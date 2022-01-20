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

from collections import OrderedDict

from requests import HTTPError

from oclcwskeyhmacsig.util import (
    post_empty_body_and_recieve_json_from_oclc_url, make_url_and_auth_header,
    get_json_from_oclc_url)

from django.conf import settings

CIRCULATION_INFO_FIELD = \
    'urn:mace:oclc.org:eidm:schema:persona:wmscircselfinfo:20180101'

class OCLCApiFail(Exception): pass

def get_oclc_access_token(authorization_code):
    url, auth_header = make_url_and_auth_header(
        settings.ILLREQUEST_OCLC_SCIM_CLIENT_ID,
        settings.ILLREQUEST_OCLC_SCIM_SECRET,
        settings.ILLREQUEST_TOKEN_REQUEST_URL,
        list(sorted(OrderedDict(
            authenticatingInstitutionId=settings.ILLREQUEST_INSTITUTION_ID,
            code=authorization_code,
            contextInstitutionId=settings.ILLREQUEST_INSTITUTION_ID,
            grant_type='authorization_code',
            ).items())),
        method='POST',
    )

    try :
        json_response = post_empty_body_and_recieve_json_from_oclc_url(
                url, auth_header
            )
    except HTTPError as e:
        raise OCLCApiFail(
            "there was a communication error with OCLC's access token "
            "request end point")

    if 'access_token' not in json_response:
        raise OCLCApiFail(
            "an access token was not found in the response from OCLC")

    return json_response['access_token']

def get_oclc_wms_simplified_patron_profile(access_token):
    try:
        me_response = get_json_from_oclc_url(
            settings.ILLREQUEST_OCLC_WMS_SCIM_ME_ENDPOINT,
            'Bearer ' + access_token,
            json_accept=False,
        )
    except HTTPError as e:
        raise OCLCApiFail(
            "There was a communication error with OCLC's WMS SCIM /Me endpoint")

    for expected_fieldname in ('name', 'email', CIRCULATION_INFO_FIELD):
        if expected_fieldname not in me_response:
            raise OCLCApiFail(
                "field name %s was not found in the OCLC SCIM api response" %
                expected_fieldname)

    if ('circulationInfo' not in me_response[CIRCULATION_INFO_FIELD] or
        'barcode' not in
        me_response[CIRCULATION_INFO_FIELD]['circulationInfo']):
        raise OCLCApiFail(
            "barcode was not found in the OCLC SCIM api response")

    if ( ('givenName' not in me_response['name']) and
         ('familyName' not in me_response['name']) ):
        raise OCLCApiFail(
            "neither givenName nor familyName was found in the OCLC SCIM api "
            "response")

    # combine givenName and familyName if available, otherwise just
    # use the one that's availalble (check above assures one)
    name = ( '' if 'givenName' not in me_response['name']
             else me_response['name']['givenName'] )
    name += ( '' if 'familyName' not in me_response['name']
              else ' ' + me_response['name']['familyName'] )
    name = name.strip()

    response_dict = {
        'name': name,
        'email': me_response['email'],
        'barcode':
        me_response[CIRCULATION_INFO_FIELD]['circulationInfo']['barcode'],
        'borrowerCategory': me_response[CIRCULATION_INFO_FIELD][
            'circulationInfo']['borrowerCategory'],
    }
    response_dict.update( { k: v
                            for k,v in me_response['name'].items()
                            if k=='givenName' or k=='familyName' } )

    return response_dict
