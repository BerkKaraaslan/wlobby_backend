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
    attribute = str(request.GET.get('attribute'))
    new_value = request.GET.get('new_value')
    retrive_dict = update_user(user_id,attribute,new_value)
    return HttpResponse(json.dumps(retrive_dict))

def update_advert_view(request):
    advertid = request.GET.get('advertid')
    attribute = str(request.GET.get('attribute'))
    new_value = request.GET.get('new_value')
    retrive_dict = update_advert(advertid, attribute, new_value)
    return HttpResponse(json.dumps(retrive_dict))

def update_user_list_attributes_view(request):
    userid = request.GET.get('id')
    attribute = str(request.GET.get('attribute'))
    value = request.GET.get('value')
    op_type = str(request.GET.get('optype'))
    retrive_dict = update_user_list_attributes(userid, attribute, value, op_type)
    return HttpResponse(json.dumps(retrive_dict))

def update_advert_list_attributes_view(request):
    advertid = request.GET.get('id')
    attribute = str(request.GET.get('attribute'))
    value = request.GET.get('value')
    op_type = str(request.GET.get('optype'))
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
    authtokens = request.GET.get('auth').split(",")
    name = str(request.GET.get('name'))
    surname = str(request.GET.get('surname'))
    username = str(request.GET.get('username'))
    sex = str(request.GET.get('sex'))
    email = str(request.GET.get('email'))
    age = int(request.GET.get('age'))
    location = str(request.GET.get('location'))
    bio = str(request.GET.get('bio'))
    profilephoto = str(request.GET.get('profilephoto'))
    likedfilms = request.GET.get('likedfilms').split(",")
    interests = request.GET.get('interests').split(",")
    about = str(request.GET.get('about'))
    retrive_dict = create_user(authtokens,name,surname,username,sex,email,age,location,bio,profilephoto,likedfilms,interests,about)
    return HttpResponse(json.dumps(retrive_dict))

def create_advert_view(request):
    try:
        ownerid = int(request.GET.get('id',''))
        if ownerid == '':
            return HttpResponse(json.dumps({'Status':'Fail','Message':'You must specify the ownerid'}))
        date = str(request.GET.get('date'))
        quota = int(request.GET.get('quota'))
        preference = str(request.GET.get('preference'))
        filmid = int(request.GET.get('filmid'))
        print("ownerid:" + ownerid)
        print("date:" + date)
        print("quota:" + quota)
        print("preference:" + preference)
        print("filmid:" + filmid)
        retrive_dict = create_advert(ownerid,date,quota,preference,filmid)
        return HttpResponse(json.dumps(retrive_dict))

    except:
        return HttpResponse(json.dumps({'Status':'Fail','Message':'You must specify the ownerid'}))


def redirection_view(request):
    response = {'Status':'Fail','Message':'This is default redirection message. You received this message because your URL is bad'}
    return HttpResponse(json.dumps(response))
    