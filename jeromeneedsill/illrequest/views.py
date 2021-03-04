from sys import stderr

from django.shortcuts import render

from .models import illrequestbase, openurlrequest

# Create your views here.
def openurl_linkresolver(request):
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
    
    return render(
        request, 'linkresolverfront.html', {} )
