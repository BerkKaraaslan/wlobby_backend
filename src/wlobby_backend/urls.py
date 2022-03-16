"""wlobby_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from django.views.static import serve # These imports are for Heroku deployment
from django.urls import re_path  # from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from homepage.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view), # Default view for our homepage
    path('get/user/',get_user_view), # user i don
    path('get/user/adverts',get_user_adverts_view), # bu user in butun advertlarini don
    path('get/users/',get_users_view), # butun userlari don
    path('get/advert/',get_advert_view), # adverti don
    path('get/adverts/',get_adverts_view),# butun advertlari don
    path('update/user/',update_user_view), # user i update et
    path('update/advert/',update_advert_view), # advert i update et
    
    # bir tane default redirection URL i koy !!!

#    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
#    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        re_path(r'^static/(?P<path>.*)$', serve, { # Comment out these lines when run on local host
            'document_root': settings.STATIC_ROOT, # comment out 
        }),                                        # comment out   ALSO comment out STATIC_ROOT on settings.py
    ]
    





