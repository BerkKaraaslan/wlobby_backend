from django.shortcuts import render
from django.http import HttpResponse
from dynamodb import *
from django.http import request
import json
# Create your views here.

def home_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    return HttpResponse(json.dumps({"Status":"Success","Message":"Server is ready to serve!"}))

def get_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid','')
        if user_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        retrieve_dict= retrieve_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def get_user_adverts_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid','')
        if user_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        retrieve_dict = retrieve_users_all_adverts(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def get_users_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    # REQUEST TYPE -> GET
    try:

        retrieve_dict = retrieve_all_users()
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def get_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid','')
        if advert_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify advertid"}))
        retrieve_dict = retrieve_advert(advert_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def get_adverts_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    # REQUEST TYPE -> GET
    try:

        retrieve_dict = retrieve_all_adverts()
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def update_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid','')
        if user_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        attribute = request.GET.get('attribute','')
        if attribute == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify attribute"}))
        new_value = request.GET.get('new_value','')
        if new_value == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify new_value"}))
        retrieve_dict = update_user(user_id,attribute,new_value)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def update_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid','')
        if advert_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify advertid"}))
        attribute = request.GET.get('attribute','')
        if attribute == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify attribute"}))
        new_value = request.GET.get('new_value','')
        if new_value == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify new_value"}))
        retrieve_dict = update_advert(advert_id, attribute, new_value)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def update_user_list_attributes_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid','')
        if user_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        attribute = request.GET.get('attribute','')
        if attribute == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify attribute"}))
        new_value = request.GET.get('new_value','')
        if new_value == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify new_value"}))
        op_type = request.GET.get('op_type','')
        if op_type == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify op_type valid op_types are add and remove"}))
        retrieve_dict = update_user_list_attributes(user_id, attribute, new_value, op_type)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def update_advert_list_attributes_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid','')
        if advert_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify advertid"}))
        attribute = request.GET.get('attribute','')
        if attribute == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify attribute"}))
        new_value = request.GET.get('new_value','')
        if new_value == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify new_value"}))
        op_type = request.GET.get('op_type','')
        if op_type == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify op_type valid op_types are add and remove"}))
        retrieve_dict = update_user_list_attributes(advert_id, attribute, new_value, op_type)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def delete_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid','')
        if user_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        retrieve_dict = delete_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def delete_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid','')
        if advert_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify advertid"}))
        retrieve_dict = delete_advert(advert_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def create_user_view(request):
    # GEREKEN PARAMETRELER

    # auth_tokens -> str list
    # name -> str
    # surname -> str
    # username -> str
    # sex -> str
    # email -> str
    # age -> int
    # location -> str
    # bio -> str
    # profile_photo -> str
    # liked_films -> int list
    # interests -> str list
    # about -> str
    # REQUEST TYPE -> GET

    # Eger Cognito tokenlari kendi iclerinde , karakteri iceriyorsa bu kodun guncellenmesi gerekir bu hali calismaz !!!
    # Cast islemini fonksiyonu cagirirken yap !!!!
    try:

        auth_tokens = request.GET.get('auth_tokens','')
        if auth_tokens == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify auth_tokens"}))
        auth_tokens = auth_tokens.split(",")
        formatted_auth_tokens = [] # dogru formatlanmis tokenlar bu list de yer alacak
        for i in range(len(auth_tokens)):
            formatted_auth_tokens.append(auth_tokens[i].replace("\"",""))
        name = request.GET.get('name','')
        if name == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify name"}))
        surname = request.GET.get('surname','')
        if surname == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify surname"}))
        username = request.GET.get('username','')
        if username == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify username"}))
        sex = request.GET.get('sex','')
        if sex == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify sex"}))
        email = request.GET.get('email','')
        if email == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify email"}))
        age = request.GET.get('age','')
        if age == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify age"}))
        location = request.GET.get('location','')
        if location == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify location"}))
        bio = request.GET.get('bio','')
        if bio == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify bio"}))
        profile_photo = request.GET.get('profile_photo','')
        if profile_photo == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify profile_photo"}))
        liked_films = request.GET.get('liked_films','')
        if liked_films == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify liked_films"}))
        liked_films = liked_films.split(",")
        formatted_liked_films = [] # dogru formatlanmis liked films ler bu list de yer alacak
        for i in range(len(liked_films)):
            formatted_liked_films.append(int(liked_films[i]))
        interests = request.GET.get('interests','')
        if interests == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify interests"}))
        interests = interests.split(",")
        formatted_interests = [] # dogru formatlanmis interests ler bu list de yer alacak
        for i in range(len(interests)):
            formatted_interests.append(interests[i].replace("\"",""))
        about = request.GET.get('about','')
        if about == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify about"}))
        retrieve_dict = create_user(formatted_auth_tokens,name,surname,username,sex,email,age,location,bio,profile_photo,formatted_liked_films,formatted_interests,about)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

def create_advert_view(request):
    # GEREKEN PARAMETRELER

    # ownerid -> int
    # date -> str
    # quota -> int
    # preference -> str
    # filmid -> int
    # REQUEST TYPE -> GET
    
    try:

        owner_id = request.GET.get('ownerid','')
        if owner_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify the ownerid"}))
        date = request.GET.get('date','')
        if date == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify date"}))
        quota = request.GET.get('quota','')
        if quota == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify quota"}))
        preference = request.GET.get('preference','')
        if preference == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify preference"}))
        film_id = request.GET.get('filmid','')
        if film_id == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify filmid"}))
        description = request.GET.get('description','')
        if description == '': # parametre verilmemis
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify description"}))
        retrieve_dict = create_advert(int(owner_id),date,int(quota),preference,int(film_id),description)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))

    
def redirection_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    try:

        response = {'Status':'Fail','Message':'This is default redirection message. You received this message because your URL is bad'}
        return HttpResponse(json.dumps(response))

    except:
        return HttpResponse(json.dumps({"Status":"Fail","Message":"An exception occured during URL parsing"}))
    
