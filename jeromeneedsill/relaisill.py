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
