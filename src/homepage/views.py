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
    print(retrieve_dict)
    return HttpResponse(json.dumps(retrieve_dict))

def get_user_adverts_view(request):
    pass

def get_users_view(request):
    pass

def get_advert_view(request):
    pass

def get_adverts_view(request):
    pass

def update_user_view(request):
    pass

def update_advert_view(request):
    pass



