from django.urls import path

from .views import openurl_requestlog_and_directtologin, post_oauth

urlpatterns = [
     path('requestlogin', openurl_requestlog_and_directtologin,
         name='requestlogin'),
    path('PostOAuth', post_oauth),
]
