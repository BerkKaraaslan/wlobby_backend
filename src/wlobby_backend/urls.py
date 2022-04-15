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

    path('get/user/',get_user_view), # user i don   GET
    path('get/user/adverts/',get_user_adverts_view), # bu user in butun advertlarini don    GET
    path('get/user/with/mail/',get_user_with_mail_view), # mail adresi ile sorgulanan useri donecek GET
    path('get/users/',get_users_view), # butun userlari don     GET
    path('get/users/with/name/surname/',get_users_with_name_and_surname_view), # name ve surname ile bulunan userlari don   GET
    path('get/advert/',get_advert_view), # adverti don  GET
    path('get/adverts/',get_adverts_view),# butun advertlari don    GET
    path('get/adverts/with/filmid/',get_adverts_with_filmid_view),      # GET
    
    path('update/user/',update_user_view), # user i update et       PUT
    path('update/advert/',update_advert_view), # advert i update et      PUT
    path('update/user/list/',update_user_list_attributes_view), # userin list attr.unu update et           PUT
    #path('update/advert/list/',update_advert_list_attributes_view), # advertin list attr.unu update et     PUT

    path('delete/user/',delete_user_view), # useri sil      DELETE
    path('delete/advert/',delete_advert_view), # adverti sil        DELETE

    path('create/user/', create_user_view), # useri yarat       POST
    path('create/advert/', create_advert_view), # adverti yarat     POST

    path('join/advert/', join_advert_view), # bu 3 request direk url den parametreleri alacak.      PUT
    path('accept/user/', accept_user_view), # PUT
    path('reject/user/', reject_user_view), # PUT


    # Bu requestlerin PUT ve POST olanlarinda parametreler http mesajının body kismindan alinacak
    # ANCAK son 3 URL haric cunku onlarda update ama onlarin URL i cok kisa!!!


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
    


# ayrica redirect loop a takiliyor !!! 
# onu cozmenin yolunu bul !!! sadece URL in son kismini degil URL in tamammini redirection a yonlendirsin
