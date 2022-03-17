import re
from django.shortcuts import render
from django.http import HttpResponse
from dynamodb import *
from django.http import request
import json
# Create your views here.

def home_view(request):
    return HttpResponse("<h1>Server is ready to serve!</h1>")

def get_user_view(request):
    user_id = request.GET.get('id')
    retrieve_dict= retrieve_user(user_id)
    #print(retrieve_dict)
    return HttpResponse(json.dumps(retrieve_dict))

def get_user_adverts_view(request):
    user_id = request.GET.get('id')
    retrive_dict = retrieve_users_all_adverts(user_id)
    return HttpResponse(json.dumps(retrive_dict))

def get_users_view(request):
    retrive_dict = retrieve_all_users()
    return HttpResponse(json.dumps(retrive_dict))

def get_advert_view(request):
    advertid = request.GET.get('advertid')
    retrive_dict = retrieve_advert(advertid)
    return HttpResponse(json.dumps(retrive_dict))

def get_adverts_view(request):
    retrive_dict = retrieve_all_adverts()
    return HttpResponse(json.dumps(retrive_dict))

def update_user_view(request):
    user_id = request.GET.get('id')
    attribute = request.GET.get('attribute')
    new_value = request.GET.get('new_value')
    retrive_dict = update_user(user_id,attribute,new_value)
    return HttpResponse(json.dumps(retrive_dict))

def update_advert_view(request):
    advertid = request.GET.get('advertid')
    attribute = request.GET.get('attribute')
    new_value = request.GET.get('new_value')
    retrive_dict = update_advert(advertid, attribute, new_value)
    return HttpResponse(json.dumps(retrive_dict))

def update_user_list_attributes_view(request):
    userid = request.GET.get('id')
    attribute = request.GET.get('attribute')
    value = request.GET.get('value')
    op_type = request.GET.get('optype')
    retrive_dict = update_user_list_attributes(userid, attribute, value, op_type)
    return HttpResponse(json.dumps(retrive_dict))

def update_advert_list_attributes_view(request):
    advertid = request.GET.get('id')
    attribute = request.GET.get('attribute')
    value = request.GET.get('value')
    op_type = request.GET.get('optype')
    retrive_dict = update_user_list_attributes(advertid, attribute, value, op_type)
    return HttpResponse(json.dumps(retrive_dict))

def delete_user_view(request):
    userid = request.GET.get('id')
    retrive_dict = delete_user(userid)
    return HttpResponse(json.dumps(retrive_dict))

def delete_advert_view(request):
    advertid = request.GET.get('advertid')
    retrive_dict = delete_advert(advertid)
    return HttpResponse(json.dumps(retrive_dict))

def create_user_view(request):
    authtokens = request.GET.get('auth')
    name = request.GET.get('name')
    surname = request.GET.get('surname')
    username = request.GET.get('username')
    sex = request.GET.get('sex')
    email = request.GET.get('email')
    age = request.GET.get('age')
    location = request.GET.get('location')
    bio = request.GET.get('bio')
    profilephoto = request.GET.get('profilephoto')
    likedfilms = request.GET.get('likedfilms')
    interests = request.GET.get('interests')
    about = request.GET.get('about')
    retrive_dict = create_user(authtokens,name,surname,username,sex,email,age,location,bio,profilephoto,likedfilms,interests,about)
    return HttpResponse(json.dumps(retrive_dict))

def create_advert_view(request):
    ownerid = request.GET.get('id')
    date = request.GET.get('date')
    quota = request.GET.get('quota')
    preference = request.GET.get('preference')
    filmid = request.GET.get('filmid')
    retrive_dict = create_advert(ownerid,date,quota,preference,filmid)
    return HttpResponse(json.dumps(retrive_dict))
    