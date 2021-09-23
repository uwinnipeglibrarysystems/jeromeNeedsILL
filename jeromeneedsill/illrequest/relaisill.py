from urllib.parse import urlencode, urljoin

from requests.exceptions import RequestException

from django.conf import settings
from django.shortcuts import redirect

from jeromeneedsill.relaisill import request_relais_authorization_id
from .rendermanualsaveprofile import render_post_oauth_manual_save_profile
from .models import openurlrequest, relaisrequestsmade

def refer_profile_and_request_to_relais(
        request, profile_id, illrbase, patron_profile):

    patron_id = profile_id

    # FIXME, REMOTE_ADDR may not be correct for all setups
    # configuration logic should be added
    if 'REMOTE_ADDR' not in request.META:
        raise Exception(
            "detection of patron ip address not available through "
            "REMOTE_ADDR field in request.META, alternative needed")
    patron_ip = request.META['REMOTE_ADDR']

    # FIXME, more investigation required to ensure this is correct
    # in most setups, configuration logic may be required
    if 'HTTP_USER_AGENT' not in request.META:
        raise Exception(
            "detection of patron user-agent not available through "
            "HTTP_USER_AGENT field in request.META, alternative needed")
    patron_useragent = request.META['HTTP_USER_AGENT']

    # development only feature, support for specifying a specific patron_id
    # to use instead of one subject to the logic producing profile_id
    if ( settings.DEBUG and
         hasattr(settings, 'RELAIS_DEBUG_PROFILE_ID_OVERRIDE') ):
        patron_id = settings.RELAIS_DEBUG_PROFILE_ID_OVERRIDE

    # development only feature, support for override of patron ip address
    # because development web server is just going to have something like
    # 127.0.0.1
    if ( settings.DEBUG and
         hasattr(settings, 'RELAIS_DEBUG_PATRON_IP_OVERRIDE') ):
        patron_ip = settings.RELAIS_DEBUG_PATRON_IP_OVERRIDE

    # development only feature, support for override of patron user-agent
    # though, if request.META['HTTP_USER_AGENT'] then most dev
    # situations shouldn't require this
    if ( settings.DEBUG and
         hasattr(settings, 'RELAIS_DEBUG_PATRON_USER_AGENT_OVERRIDE') ):
        patron_useragent = settings.RELAIS_DEBUG_PATRON_USER_AGENT_OVERRIDE

    try:
        relais_aid_response_json = request_relais_authorization_id(
            settings.RELAIS_PORTAL_HOST, # server_host
            settings.RELAIS_SYMBOL, # librarysymbol
            settings.RELAIS_AUTH_API_KEY, # apikey
            patron_id=patron_id, # patron_id
            enduser_ip=patron_ip,
            enduser_useragent=patron_useragent,
            partnership_id=(
                None if not hasattr(settings, 'RELAIS_PARTNERSHIP_OVERRIDE')
                else settings.RELAIS_PARTNERSHIP_OVERRIDE)
        )
    except RequestException as e:
        return render_post_oauth_manual_save_profile(
            request, illrbase, patron_profile,
            error='communication error with relais portal')

    # if Relais does not give us an authorization id for some reason
    # then we need to process the profile and request manually
    if 'AuthorizationId' not in relais_aid_response_json:
        return render_post_oauth_manual_save_profile(
            request, illrbase, patron_profile,
            error='authorization id was not obtained')

    urlparams = (
        # TODO: also saw authzid in some docs, but that doesn't seem to
        # get the same results
        # https://help.oclc.org/Resource_Sharing/Relais_ILL/Relais_Portal/Relais_Portal_FAQ
        ('LS', settings.RELAIS_SYMBOL),
        ('group', 'patron'),
        ('aid', relais_aid_response_json['AuthorizationId']),
    )

    urlparams += tuple( (
        (openurlrequest.key, openurlrequest.value)
        for openurlrequest in openurlrequest.objects.filter(request=illrbase)
    ) )

    # keep a record that we went as far as successfully getting a aid
    # from relais for our user and that we're about to redirect them to
    # relais portal with that aid
    #
    # Ideally we would just delete the illrbase and openurlrequest database
    # entries at this point, or after a return from portal
    # but we don't what will happen to our patron once they get there as there
    # is no return back.
    #
    # So, we keep a record of getting this far and we can do automated
    # database clean-up jobs down the road which will delete connected
    # illrbase, relaisrequestsmade, and openurlrequest entries once they
    # are old enough
    rrm = relaisrequestsmade(
        request=illrbase,
        # not patron_id, as that is likely profile_id
        # which postoauth.py may have made a UUID
        barcode=patron_profile['barcode'],
        # value sent to Relais in X-Real-IP
        # enduser_ip arg to request_relais_authorization_id
        ip=patron_ip,
    )
    rrm.save()

    return redirect(
        urljoin(
            settings.RELAIS_PORTAL_BASE_URL,
            "/user/login.html"
            ) + "?" + urlencode(urlparams)
        )
