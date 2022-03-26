from django.shortcuts import render
from django.http import HttpResponse
from dynamodb import *
from django.http import request
import json
from decouple import config
import base64
import requests
from .decode_jwt import *


def login(request):
    try:
        code = request.GET.get('code')
        userdata = getTokens(code)
        response = HttpResponse(json.dumps({"Status": "Success", "Message": "User data passed", "User_data": userdata}))
        response.set_cookie('sessiontoken', userdata['id_token'], max_age=24 * 60 * 60, httponly=True)
        return response
    except:
        token = getSession(request)

        if token is not None:
            userdata =lambda_handler(token, None)
            response = HttpResponse(json.dumps({"Status": "Success", "Message": "User data passed", "User_data": userdata}))
        return response


def getTokens(code):
    TOKEN_END_POINT = config('TOKEN_END_POINT')
    REDIRECT_URI = config('REDIRECT_URI')
    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRET')

    token_url = TOKEN_END_POINT
    message = bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", 'utf-8')
    secret_hash = base64.b64encode(message).decode()
    payload = {
        "grant_type": 'authorization_code',
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": f"Basic {secret_hash}"}

    response = requests.post(token_url, params=payload, headers=headers)

    # response will return id token, access token and refresh token
    id_token = response.json()['id_token']
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']
    #user_Data = decode_jwt.lamda_handler({'token': id_token}, None)

    event={'token' : id_token}
    user_Data=lambda_handler(event,None)

    if not user_Data:
        return False

    user = {
        'name': user_Data['name'],
        'email': user_Data['email'],
        'id_token': id_token,
        'access_token' :access_token
    }

    return user


def getSession(request):
    try:
        response = request.COOKIES["sessiontoken"]
        return response
    except:
        return None


def home_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    return HttpResponse(json.dumps({"Status": "Success", "Message": "Server is ready to serve!"}))


def get_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))
        retrieve_dict = retrieve_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_user_adverts_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))
        retrieve_dict = retrieve_users_all_adverts(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_user_with_mail_view(request):
    # GEREKEN PARAMETRELER

    # email -> str
    # REQUEST TYPE -> GET
    try:

        email = request.GET.get('Email', '')
        if email == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify Email"}))
        retrieve_dict = retrieve_user_with_email(email)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_users_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    # REQUEST TYPE -> GET
    try:

        retrieve_dict = retrieve_all_users()
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_users_with_name_and_surname_view(request):
    # GEREKEN PARAMETRELER

    # name -> str (optional)  surname -> str (optional)
    # REQUEST TYPE -> GET

    # kontrol fonksiyonda yapiliyor burada eger parametre yoksa None gonderilecek
    try:

        name = request.GET.get('Name', '')
        if name == '':  # parametre verilmemis
            name = None
        surname = request.GET.get('Surname', '')
        if surname == '':  # parametre verilmemis
            surname = None

        retrieve_dict = retrieve_all_users_with_name_and_surname(name, surname)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('AdvertID', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify AdvertID"}))
        retrieve_dict = retrieve_advert(advert_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_adverts_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    # REQUEST TYPE -> GET
    try:

        retrieve_dict = retrieve_all_adverts()
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_adverts_with_filmid_view(request):
    # GEREKEN PARAMETRELER

    # filmid -> int
    # REQUEST TYPE -> GET
    try:

        filmid = request.GET.get('FilmID', '')
        if filmid == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify FilmID"}))
        retrieve_dict = retrieve_all_adverts_with_filmid(filmid)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def update_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "UserID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify UserID"}))

        user_id = request_parameters["UserID"]

        if "Attribute" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Attribute"}))

        attribute = request_parameters["Attribute"]

        if "NewValue" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify NewValue"}))

        new_value = request_parameters["NewValue"]

        retrieve_dict = update_user(user_id,attribute,new_value)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def update_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "AdvertID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify AdvertID"}))

        advert_id = request_parameters["AdvertID"]

        if "Attribute" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Attribute"}))

        attribute = request_parameters["Attribute"]

        if "NewValue" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify NewValue"}))

        new_value = request_parameters["NewValue"]

        retrieve_dict = update_advert(advert_id,attribute,new_value)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def update_user_list_attributes_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "UserID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify UserID"}))

        user_id = request_parameters["UserID"]

        if "Attribute" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Attribute"}))

        attribute = request_parameters["Attribute"]

        if "NewValue" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify NewValue"}))

        new_value = request_parameters["NewValue"]

        if "OpType" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify OpType valid OpTypes are add and remove"}))

        op_type = request_parameters["OpType"]

        retrieve_dict = update_user_list_attributes(user_id,attribute,new_value,op_type)
        return HttpResponse(json.dumps(retrieve_dict))


    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def update_advert_list_attributes_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "AdvertID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify AdvertID"}))

        advert_id = request_parameters["AdvertID"]

        if "Attribute" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Attribute"}))

        attribute = request_parameters["Attribute"]

        if "NewValue" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify NewValue"}))

        new_value = request_parameters["NewValue"]

        if "OpType" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify OpType valid OpTypes are add and remove"}))

        op_type = request_parameters["OpType"]

        retrieve_dict = update_advert_list_attributes(advert_id,attribute,new_value,op_type)
        return HttpResponse(json.dumps(retrieve_dict))


    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def delete_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))
        retrieve_dict = delete_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def delete_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('AdvertID', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify AdvertID"}))
        retrieve_dict = delete_advert(advert_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


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

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "Email" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Email"}))

        email = request_parameters["Email"]

        if "CognitoAuthTokens" not in request_parameters.keys():
            authtokens = None
        else:
            authtokens = request_parameters["CognitoAuthTokens"]

        if "Name" not in request_parameters.keys():
            name = None
        else:
            name = request_parameters["Name"]
       
        if "Surname" not in request_parameters.keys():
            surname = None
        else:
            surname = request_parameters["Surname"]

        if "Username" not in request_parameters.keys():
            username = None
        else:
            username = request_parameters["Username"]
        
        if "Sex" not in request_parameters.keys():
            sex = None
        else:
            sex = request_parameters["Sex"]

        if "Age" not in request_parameters.keys():
            age = None
        else:
            age = request_parameters["Age"]

        if "Location" not in request_parameters.keys():
            location = None
        else:
            location = request_parameters["Location"]

        if "Bio" not in request_parameters.keys():
            bio = None
        else:
            bio = request_parameters["Bio"]

        if "ProfilePhoto" not in request_parameters.keys():
            profilephoto = None
        else:
            profilephoto = request_parameters["ProfilePhoto"]

        if "LikedFilms" not in request_parameters.keys():
            likedfilms = None
        else:
            likedfilms = request_parameters["LikedFilms"]

        if "Interests" not in request_parameters.keys():
            interests = None
        else:
            interests = request_parameters["Interests"]

        if "About" not in request_parameters.keys():
            about = None
        else:
            about = request_parameters["About"]


        retrieve_dict = create_user(email,authtokens=authtokens,name=name,surname=surname,username=username,sex=sex,age=age,location=location,bio=bio,profilephoto=profilephoto,likedfilms=likedfilms,interests=interests,about=about)
        return HttpResponse(json.dumps(retrieve_dict))


    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def create_advert_view(request):
    # GEREKEN PARAMETRELER

    # ownerid -> int
    # date -> str
    # quota -> int
    # preference -> str
    # filmid -> int
    # REQUEST TYPE -> GET

    try:

        request_parameters = json.loads(request.body.decode("utf-8"))

        if "OwnerID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify OwnerID"}))

        owner_id = request_parameters["OwnerID"]

        if "Date" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Date"}))

        date = request_parameters["Date"]

        if "Quota" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Quota"}))

        quota = request_parameters["Quota"]

        if "AttendeePreference" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify AttendeePreference"}))

        preference = request_parameters["AttendeePreference"]

        if "FilmID" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify FilmID"}))

        film_id = request_parameters["FilmID"]

        if "Description" not in request_parameters.keys():
            return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify Description"}))

        description = request_parameters["Description"]


        retrieve_dict = create_advert(owner_id, date, quota, preference, film_id, description)
        return HttpResponse(json.dumps(retrieve_dict))


    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def join_advert_view(request):  # Bu bir update islemi ama parametreler cok kucuk oldugu icin direk url den okuyacak
    # GEREKEN PARAMETRELER

    # advertid -> int
    # userid -> int
    # REQUEST TYPE -> GET

    try:

        advert_id = request.GET.get('AdvertID', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the AdvertID"}))
        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))

        retrieve_dict = join_advert(advert_id, user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def accept_user_view(request):  # Bu bir update islemi ama parametreler cok kucuk oldugu icin direk url den okuyacak
    # GEREKEN PARAMETRELER

    # advertid -> int
    # userid -> int
    # REQUEST TYPE -> GET

    try:

        advert_id = request.GET.get('AdvertID', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the AdvertID"}))
        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))

        retrieve_dict = accept_user(advert_id, user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def reject_user_view(request):  # Bu bir update islemi ama parametreler cok kucuk oldugu icin direk url den okuyacak
    # GEREKEN PARAMETRELER

    # advertid -> int
    # userid -> int
    # REQUEST TYPE -> GET

    try:

        advert_id = request.GET.get('AdvertID', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the AdvertID"}))
        user_id = request.GET.get('UserID', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify UserID"}))

        retrieve_dict = reject_user(advert_id, user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def redirection_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    try:

        response = {'Status': 'Fail', 'Message': 'This is default redirection message. You received this message because your URL is bad'}
        return HttpResponse(json.dumps(response))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))
