"""jeromeneedsill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .illrequest.nciplookupuser import ncip_lookup_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('linkresolver/',
         include('jeromeneedsill.illrequest.openurl_linkresolver_urls') ),
    path('ill/', include('jeromeneedsill.illrequest.ill_urls') ),

    # NOTE, this path should be protected and only made available to
    # a Relais ILL server
    path('nciplookupuser/', ncip_lookup_user),
]
