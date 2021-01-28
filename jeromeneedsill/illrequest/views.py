from django.shortcuts import render

# Create your views here.
def openurl_linkresolver(request):
    return render(
        request, 'linkresolverfront.html', {} )
