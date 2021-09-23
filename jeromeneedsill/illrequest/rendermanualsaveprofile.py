from django.shortcuts import render

from .models import openurlrequest, illmanualrequester

# FIXME, this should really have an error paramater for situations where
# we're calling this because of an error trying to avoid a manual entry
# vs situations where this is done because the configuration doesn't
# establish that automatic injection into something like Relais
#
# an error could be displayed to users in those cases to let them know
# their request may take a bit more to process
#
# and additional handling can occur in the error cases such as staff
# notification
def render_post_oauth_manual_save_profile(
        request, illrbase, patron_profile, error=None):
    requester = illmanualrequester(
        request=illrbase,
        requester_name=patron_profile['name'],
        email=patron_profile['email'],
        barcode=patron_profile['barcode'] )
    requester.save()

    params = openurlrequest.objects.filter(request=illrbase)

    return render(
        request, 'ill_success_with_patron_details.html',
        {'patron_profile': patron_profile,
         'error': error,
         'params': params,
        } )
