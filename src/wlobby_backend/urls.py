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

from django.urls import re_path
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view), # Default view for our homepage
    path('login/', login),
    path('get/user/',get_user_view), # user i don
    path('get/user/adverts/',get_user_adverts_view), # bu user in butun advertlarini don
    path('get/user/with/mail/',get_user_with_mail_view), # mail adresi ile sorgulanan useri donecek
    path('get/users/',get_users_view), # butun userlari don
    path('get/users/with/name/surname/',get_users_with_name_and_surname_view), # name ve surname ile bulunan userlari don
    path('get/advert/',get_advert_view), # adverti don
    path('get/adverts/',get_adverts_view),# butun advertlari don
    path('get/adverts/with/filmid/',get_adverts_with_filmid_view),
    
    path('update/user/',update_user_view), # user i update et
    path('update/advert/',update_advert_view), # advert i update et
    path('update/user/list/',update_user_list_attributes_view), # userin list attr.unu update et
    path('update/advert/list/',update_advert_list_attributes_view), # advertin list attr.unu update et

    path('delete/user/',delete_user_view), # useri sil
    path('delete/advert/',delete_advert_view), # adverti sil

    path('create/user/', create_user_view), # useri yarat
    path('create/advert/', create_advert_view), # adverti yarat

    path('join/advert/', join_advert_view), # bu 3 request direk url den parametreleri alacak.
    path('accept/user/', accept_user_view),
    path('reject/user/', reject_user_view),



   

    # request lerde body byte string oluyor yanilmiyorsam.
    # byte string -> string -> json (veya dict) e cevrilip direk attributelar alinacak


    # update ve createlerde body den mesaj alinacak

   



    # URL lerde PUT ve POST requesti geldiğinde parametreleri URL den değil requestin body sinden okuyacak hale getir.
    # ayrıca omer ile wp ye gore request tiplerini de duzelt hepsi GET olmayacak tabi ki
    # body den json falan alip onu dicitonary ye cevirme yontemlerine bak
    # faydali bir link https://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request


    path('redirection/', redirection_view),
    re_path(r'^.*$', RedirectView.as_view(url='redirection/', permanent=False), name='index') # This line redirects all wrong URL's to redirection page

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
    





# sonda slash / olmamali
# ayrica redirect loop a takiliyor !!! 
# onu cozmenin yolunu bul !!! sadece URL in son kismini degil URL in tamammini redirection a yonlendirsin
