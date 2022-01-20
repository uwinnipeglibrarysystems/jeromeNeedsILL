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

import requests

def request_relais_authorization_id(
        server_host, librarysymbol, apikey, patron_id,
        enduser_ip=None, enduser_useragent=None,
        partnership_id=None,
):
    url = "https://%s/portal-service/user/authentication" % server_host
    headers = {
        'Content-Type': 'application/json',
        }
    if enduser_ip!=None:
        headers['X-Real-IP'] = enduser_ip
    if enduser_useragent!=None:
        headers['User-Agent'] = enduser_useragent

    json = {
        'ApiKey': apikey,
        'UserGroup': 'patron',
        'LibrarySymbol': librarysymbol,
        'PatronId': patron_id,
    }
    if partnership_id!=None:
        json['PartnershipId'] = partnership_id

    r = requests.post(
        url,
        headers=headers,
        json=json,
        )
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    server = input("server > ").strip()
    libsym = input("library symbol > ").strip()
    apikey = input("api key > ").strip()
    patron_id = input("patron id > ").strip()
    partnership_id = input("partnership id (blank for none) > ").strip()
    response_json = request_relais_authorization_id(
        server, libsym, apikey, patron_id,
        partnership_id=(None if partnership_id=='' else partnership_id)
    )
    aid = (None if 'AuthorizationId' not in response_json
           else response_json['AuthorizationId'] )
    if aid!=None:
        print(aid)
        print(response_json)
