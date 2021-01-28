from django.urls import path

from .views import openurl_linkresolver

urlpatterns = [
    path('', openurl_linkresolver, name='linkresolver')
]
