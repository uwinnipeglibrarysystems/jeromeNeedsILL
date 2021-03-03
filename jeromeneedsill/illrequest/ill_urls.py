from django.urls import path

from .views import openurl_requestlog_and_directtologin

urlpatterns = [
     path('/requestlogin', openurl_requestlog_and_directtologin,
         name='requestlogin'),
]
