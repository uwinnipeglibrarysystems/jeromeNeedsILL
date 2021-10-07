from django.urls import path

from .views import \
    log_ip_and_directtologin, openurl_requestlog_and_directtologin, post_oauth

urlpatterns = [
    path('requestlogin', openurl_requestlog_and_directtologin,
         name='requestlogin'),
    path('requestloginwiplog', log_ip_and_directtologin,
         name='requestloginwiplog'),
    path('PostOAuth', post_oauth),
]
