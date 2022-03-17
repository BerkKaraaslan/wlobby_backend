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
