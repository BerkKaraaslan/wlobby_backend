from django.shortcuts import render

# Create your views here.
from decouple import config
import base64
import requests
from mylobby import decode_jwt
from django.http import HttpResponse
import json




def home_view(request):
    try:
        code=request.GET.get('code')
        userdata=getTokens(code)
        response=HttpResponse(json.dumps({"Status":"Success","Message":"User infos pass","User_data":userdata}))
        response.set_cookie('sessiontoken',userdata['id_token'],max_age=24*60*60,httponly=True)
        return response
    except:
        token=getSession(request)

        if token is not None:
            userdata=decode_jwt.lamda_handler(token,None)
            response = HttpResponse(json.dumps({"Status": "Success", "Message": "User infos pass", "User_data": userdata}))
        return token







def getTokens(code):
    TOKEN_END_POINT=config('TOKEN_END_POINT')
    REDIRECT_URI=config('REDIRECT_URI')
    CLIENT_ID=config('CLIENT_ID')
    CLIENT_SECRET=config('CLIENT_SECRET')

    encodeData=base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}","ISO-8859-1")).decode("ascii")

    headers={
        'Content-Type':'application/x-ww-form-urlencoded',
        'Authorization':f'Basic{encodeData}'
    }

    body={
        'grant_type':'authorization_code',
        'client_id':CLIENT_ID,
        'code':code,
        'redirect_uri':REDIRECT_URI
    }

    response =requests.post(TOKEN_END_POINT,data=body,headers=headers)

    #response will return id token, access token and refresh token
    id_token=response.json()['id_token']
    user_Data=decode_jwt.lamda_handler(id_token,None)

    if not user_Data:
        return False

    user={
        'id_token':id_token,
        'name':user_Data['name'],
        'email':user_Data['email']
    }

    return user


def getSession(request):
    try:
        response=request.COOKIES["sessiontoken"]
        return response
    except:
        return None


