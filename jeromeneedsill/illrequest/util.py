# careful, REMOTE_ADDR may not be correct for all setups
# configuration logic may need to be added
def get_client_ip_addr_from_request(request):
    if 'REMOTE_ADDR' not in request.META:
        raise Exception(
            "detection of patron ip address not available through "
            "REMOTE_ADDR field in request.META, alternative needed")

    return request.META['REMOTE_ADDR']
