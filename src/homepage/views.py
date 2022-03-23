from django.shortcuts import render
from django.http import HttpResponse
from dynamodb import *
from django.http import request
import json
# Create your views here.


from django.shortcuts import render

# Create your views here.
from decouple import config
import base64
import requests
from homepage import decode_jwt


def login(request):
    try:
        code = request.GET.get('code')
        userdata = getTokens(code)
        print('fff')
        response = HttpResponse(json.dumps({"Status": "Success", "Message": "User infos pass", "User_data": userdata}))
        response.set_cookie('sessiontoken', userdata['id_token'], max_age=24 * 60 * 60, httponly=True)
        return response
    except:
        token = getSession(request)

        if token is not None:
            userdata = decode_jwt.lamda_handler(token, None)
            response = HttpResponse(
                json.dumps({"Status": "Success", "Message": "User infos pass", "User_data": userdata}))
        return response


def getTokens(code):
    TOKEN_END_POINT = config('TOKEN_END_POINT')
    REDIRECT_URI = config('REDIRECT_URI')
    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRET')

    encodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic{encodeData}'
    }

    body = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_END_POINT, data=body, headers=headers)
    print(response)
    # response will return id token, access token and refresh token
    id_token = response.json()['id_token']
    user_Data = decode_jwt.lamda_handler(id_token, None)

    if not user_Data:
        return False

    user = {
        'id_token': id_token,
        'name': user_Data['name'],
        'email': user_Data['email']
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
    print(request.body)
    try:

        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))
        retrieve_dict = retrieve_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_user_adverts_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))
        retrieve_dict = retrieve_users_all_adverts(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def get_user_with_mail_view(request):
    # GEREKEN PARAMETRELER

    # email -> str
    # REQUEST TYPE -> GET
    try:

        email = request.GET.get('email', '')
        if email == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify email"}))
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

        name = request.GET.get('name', '')
        if name == '':  # parametre verilmemis
            name = None
        surname = request.GET.get('surname', '')
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

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify advertid"}))
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

        filmid = request.GET.get('filmid', '')
        if filmid == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify filmid"}))
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

        # user_id = request.GET.get('userid','')
        # if user_id == '': # parametre verilmemis
        #    return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify userid"}))
        # attribute = request.GET.get('attribute','')
        # if attribute == '': # parametre verilmemis
        #    return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify attribute"}))
        # new_value = request.GET.get('new_value','')
        # if new_value == '': # parametre verilmemis
        #    return HttpResponse(json.dumps({"Status":"Fail","Message":"You must specify new_value"}))
        # retrieve_dict = update_user(user_id,attribute,new_value)
        # return HttpResponse(json.dumps(retrieve_dict))

        parameters = json.loads(request.body.decode(
            "utf-8"))  # bu sekilde gelen requestin body sinde json formatında bulunan seyi dict olarak aldik

        # parameters in type i dict olarak elimizde !!!
        # direk parameters["userid"] seklinde ulasilabilir

        return HttpResponse(json.dumps({"Status": "Success", "Message": "This is the dummy answer"}))


    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def update_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # attribute -> str
    # new_value -> herhangi bir type
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify advertid"}))
        attribute = request.GET.get('attribute', '')
        if attribute == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify attribute"}))
        new_value = request.GET.get('new_value', '')
        if new_value == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify new_value"}))
        retrieve_dict = update_advert(advert_id, attribute, new_value)
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

        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))
        attribute = request.GET.get('attribute', '')
        if attribute == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify attribute"}))
        new_value = request.GET.get('new_value', '')
        if new_value == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify new_value"}))
        op_type = request.GET.get('op_type', '')
        if op_type == '':  # parametre verilmemis
            return HttpResponse(
                json.dumps({"Status": "Fail", "Message": "You must specify op_type valid op_types are add and remove"}))
        retrieve_dict = update_user_list_attributes(user_id, attribute, new_value, op_type)
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

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify advertid"}))
        attribute = request.GET.get('attribute', '')
        if attribute == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify attribute"}))
        new_value = request.GET.get('new_value', '')
        if new_value == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify new_value"}))
        op_type = request.GET.get('op_type', '')
        if op_type == '':  # parametre verilmemis
            return HttpResponse(
                json.dumps({"Status": "Fail", "Message": "You must specify op_type valid op_types are add and remove"}))
        retrieve_dict = update_advert_list_attributes(advert_id, attribute, new_value, op_type)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def delete_user_view(request):
    # GEREKEN PARAMETRELER

    # userid -> int
    # REQUEST TYPE -> GET
    try:

        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))
        retrieve_dict = delete_user(user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def delete_advert_view(request):
    # GEREKEN PARAMETRELER

    # advertid -> int
    # REQUEST TYPE -> GET
    try:

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify advertid"}))
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

    # Burasi update edilecek !!!!!!

    try:

        auth_tokens = request.GET.get('auth_tokens', '')
        if auth_tokens == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify auth_tokens"}))
        auth_tokens = auth_tokens.split(",")
        formatted_auth_tokens = []  # dogru formatlanmis tokenlar bu list de yer alacak
        for i in range(len(auth_tokens)):
            formatted_auth_tokens.append(auth_tokens[i].replace("\"", ""))
        name = request.GET.get('name', '')
        if name == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify name"}))

        # artik zorunlu olmayan attributelarda bu hatayi vermeyecek
        # ornek
        # if name == '': # parametre verilmemis
        #    name = None # bu sayede fonksiyona verince default argumanla ayni oldugu icin user a name koymayacak
        # else durumunda bir sey yapilmayacak
        # cunku zaten argumanin bir degeri var !!!

        surname = request.GET.get('surname', '')
        if surname == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify surname"}))
        username = request.GET.get('username', '')
        if username == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify username"}))
        sex = request.GET.get('sex', '')
        if sex == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify sex"}))
        email = request.GET.get('email', '')
        if email == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify email"}))
        age = request.GET.get('age', '')
        if age == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify age"}))
        location = request.GET.get('location', '')
        if location == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify location"}))
        bio = request.GET.get('bio', '')
        if bio == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify bio"}))
        profile_photo = request.GET.get('profile_photo', '')
        if profile_photo == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify profile_photo"}))
        liked_films = request.GET.get('liked_films', '')
        if liked_films == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify liked_films"}))
        liked_films = liked_films.split(",")
        formatted_liked_films = []  # dogru formatlanmis liked films ler bu list de yer alacak
        for i in range(len(liked_films)):
            formatted_liked_films.append(int(liked_films[i]))
        interests = request.GET.get('interests', '')
        if interests == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify interests"}))
        interests = interests.split(",")
        formatted_interests = []  # dogru formatlanmis interests ler bu list de yer alacak
        for i in range(len(interests)):
            formatted_interests.append(interests[i].replace("\"", ""))
        about = request.GET.get('about', '')
        if about == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify about"}))
        retrieve_dict = create_user(formatted_auth_tokens, name, surname, username, sex, email, age, location, bio,
                                    profile_photo, formatted_liked_films, formatted_interests, about)
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

        owner_id = request.GET.get('ownerid', '')
        if owner_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the ownerid"}))
        date = request.GET.get('date', '')
        if date == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify date"}))
        quota = request.GET.get('quota', '')
        if quota == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify quota"}))
        preference = request.GET.get('preference', '')
        if preference == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify preference"}))
        film_id = request.GET.get('filmid', '')
        if film_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify filmid"}))
        description = request.GET.get('description', '')
        if description == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify description"}))
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

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the advertid"}))
        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))

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

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the advertid"}))
        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))

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

        advert_id = request.GET.get('advertid', '')
        if advert_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify the advertid"}))
        user_id = request.GET.get('userid', '')
        if user_id == '':  # parametre verilmemis
            return HttpResponse(json.dumps({"Status": "Fail", "Message": "You must specify userid"}))

        retrieve_dict = reject_user(advert_id, user_id)
        return HttpResponse(json.dumps(retrieve_dict))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))


def redirection_view(request):
    # GEREKEN PARAMETRELER

    # YOK
    try:

        response = {'Status': 'Fail',
                    'Message': 'This is default redirection message. You received this message because your URL is bad'}
        return HttpResponse(json.dumps(response))

    except:
        return HttpResponse(json.dumps({"Status": "Fail", "Message": "An exception occured during URL parsing"}))
