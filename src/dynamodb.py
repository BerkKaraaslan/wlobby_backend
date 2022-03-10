import boto3

from id_generator import *
from current_time import *


with open('access_keys.txt') as f:
    lines = f.readlines()

AWS_ACCESS_KEY_ID = lines[0].rstrip()
AWS_SECRET_ACCESS_KEY = lines[1].rstrip()
DEFAULT_REGION = "us-east-1" # AWS wants a region. In my case it is "us-east-1"

client = boto3.client('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = DEFAULT_REGION)


# burada bir fonksiyon olacak connect gibi bir isimde ve program baslayinca o 1 defa cagrilacak
# her seferinde dosyadan okuma ve db ye baglanma islemleri yapilmayacak


def connect():
    pass



def format_db_item(item): # Bu fonksiyon user ve advertleri istenen formata cevirir
                          # Parametre olarak bir dictionary alir ve cevap olarak yine bir dictionary doner

    formatted_item = {}

    for key in item.keys():
        dictionary_value = item[key]
        tmp_value = list(dictionary_value.keys())
        tmp_value = tmp_value[0]
        real_value = dictionary_value[tmp_value]
        
        if tmp_value == "N": # Cast if necessary
            real_value = int(real_value)

        formatted_item[key] = real_value
        
        if type(real_value) is list:
            list_items = []
            for value in real_value:
                if list(value.keys())[0] == "N": # Cast if necessary
                    tmp = int(list(value.values())[0])
                else:
                    tmp = list(value.values())[0]

                list_items.append(tmp)
            
            formatted_item[key] = list_items

    return formatted_item



""" def test_format_user():
    

    select_statement = "SELECT * FROM FakeAdvert WHERE AdvertID=1"

    
    response = client.execute_statement(Statement=select_statement) 

    formatted_response = format_user(response["Items"][0])

    #formatted_response = format_user({}) 

    print("This is type of formatted response:" + str(type(formatted_response)))
    print()
    #print(formatted_response)

    for key in formatted_response.keys():
        print(formatted_response[key])
        print("This is type of a value" + str(type(formatted_response[key])))
        print()
        print()


    # sadece list veya set olanlarda yaziyor
    # list ler icin direk dictionary nin values() yapilabilir
    # her dict icin values cagirilir ve bunlar bir list te tutulup en son nihai value olarak bizim key e yazilir

    # o list icinde gezip her dict icin values()[0] i diyecegiz. 

 """











# CRUD Functions




# CREATE Functions





INITIAL_LOGIN_VALUE = 1 # Login count bunu tutacak

def create_user(authtokens,name,surname,username,sex,email,age,location,bio,profilephoto,likedfilms,interests,about):
    # PARAMETER TYPES

    # authtokens -> string list
    # name -> str
    # surname -> str
    # username -> str
    # sex -> str
    # email -> str
    # age -> int
    # location -> str
    # bio -> str
    # profilephoto -> str
    # likedfilms -> integer list
    # interests -> string list
    # about -> str

    try:

        user_id = get_user_id()
        increment_user_id()
        advert_ids = [] # Initially an empty list
        watched_films = []
        registration_date = curr_time()
        last_log_in = registration_date # Initially they are equal
        log_in_count = INITIAL_LOGIN_VALUE
        last_update_date = registration_date # Initially they are equal

        TABLE_NAME = 'FakeUser'
        item = f"'UserID': {user_id}, 'CognitoAuthTokens': {authtokens}, 'Name': {name}, 'Surname': {surname}, 'Username': {username}, 'AdvertIDs': {advert_ids}, 'Sex': {sex}, 'Email': {email}, 'Age': {age}, 'Location': {location}, 'Bio': {bio}, 'ProfilePhoto': {profilephoto}, 'LikedFilms': {likedfilms}, 'WatchedFilms': {watched_films}, 'RegistrationDate': {registration_date}, 'LastLogIn': {last_log_in},  'LogInCount': {log_in_count}, 'Interests': {interests}, 'About': {about}, 'LastUpdateDate': {last_update_date}"
        insert_statement = f"INSERT INTO {TABLE_NAME} VALUE" + "{" + item + "}"

        result_dict = {} # bunun icine status, message gibi attribute lar koy.
        # user ıd vs de bunun icinde donulecek

        response = client.execute_statement(Statement=insert_statement) 
        #response["Items"]  normalde birsey donmemesi lazim

    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    
    result_dict["Status"] = "Success"
    result_dict["Message"] = f"New user successfully created with user id:{user_id}"
    result_dict["UserID"] = user_id
    return result_dict




def create_advert(ownerid,date,quota,preference,filmid):
    # PARAMETER TYPES

    # ownerid -> int
    # date -> str
    # quota -> int
    # preference -> str
    # filmid -> int
    
    try:

        advert_id = get_advert_id()
        increment_advert_id()
        registration_date = curr_time()
        last_update_date = registration_date # Initially they are equal
        attendee_ids = []
        attendee_ids.append(ownerid)
        status = "active"

        TABLE_NAME = 'FakeAdvert'
        item = f"'AdvertID': {advert_id}, 'OwnerID': {ownerid}, 'Date': {date}, 'RegistrationDate': {registration_date}, 'LastUpdateDate': {last_update_date}, 'Quota': {quota}, 'AttendeePreference': {preference}, 'AttendeeIDs': {attendee_ids}, 'Status': {status}, 'FilmID': {filmid}"
        insert_statement = f"INSERT INTO {TABLE_NAME} VALUE" + "{" + item + "}"

        result_dict = {} 

        response = client.execute_statement(Statement=insert_statement) 
        #response["Items"]  normalde birsey donmemesi lazim

    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    
    result_dict["Status"] = "Success"
    result_dict["Message"] = f"New advert successfully created with advert id:{advert_id}"
    result_dict["AdvertID"] = advert_id
    return result_dict



# RETRIEVE Functions





# bu fonksiyon bir dictionary doner
# bu dictionary de "Status" islemin durumunu
# "Message" aciklamayi
# "Item" ise eger varsa o id ile bulunan user i bir dictionary olarak doner
# "UserID" eger user bulunamadi ise bu attribute hangi id (parametre) ile bulunamadigini gosterir

def retrieve_user(userid):
    # PARAMETER TYPES

    # userid -> int

    try:
        TABLE_NAME = "FakeUser"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE UserID={userid}"
        response = client.execute_statement(Statement=select_statement)
        user = response["Items"]

        result_dict = {}

        if len(user) == 0: # No such user exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such user exist with user id:{userid}"
            result_dict["UserID"] = userid
            return result_dict
        else: # User exist
            result_dict["Status"] = "Success"
            result_dict["Message"] = f"User with user id:{userid} successfully retrieved"
            user = format_db_item(user[0])
            result_dict["Item"] = user
            return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


# bu fonksiyon bir dictionary doner
# bu dictionary de "Status" islemin durumunu
# "Message" aciklamayi
# "Item" ise eger varsa o id ile bulunan advert i bir dictionary olarak doner
# "AdvertID" eger advert bulunamadi ise bu attribute hangi id (parametre) ile bulunamadigini gosterir

def retrieve_advert(advertid):
    # PARAMETER TYPES

    # advertid -> int

    try:
        TABLE_NAME = "FakeAdvert"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE AdvertID={advertid}"
        response = client.execute_statement(Statement=select_statement)
        advert = response["Items"]

        result_dict = {}

        if len(advert) == 0: # No such user exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such advert exist with advert id:{advertid}"
            result_dict["AdvertID"] = advertid
            return result_dict
        else: # User exist
            result_dict["Status"] = "Success"
            result_dict["Message"] = f"Advert with advert id:{advertid} successfully retrieved"
            advert = format_db_item(advert[0])
            result_dict["Item"] = advert
            return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}



# bu fonksiyon bir dictionary doner
# bu dictionary de "Status" islemin durumunu
# "Message" aciklamayi
# "Item" ise eger varsa o id ile bulunan userin "AdvertIDs" listesini icerir
# "UserID" eger user bulunamadi ise bu attribute hangi id (parametre) ile bulunamadigini gosterir

def retrieve_all_adverts(userid):
    # PARAMETER TYPES

    # userid -> int

    try:
        TABLE_NAME = "FakeUser"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE UserID={userid}"
        response = client.execute_statement(Statement=select_statement)
        user = response["Items"]

        result_dict = {}

        if len(user) == 0: # No such user exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such user exist with user id:{userid}"
            result_dict["UserID"] = userid
            return result_dict
        else: # User exist
            result_dict["Status"] = "Success"
            result_dict["Message"] = f"User with user id:{userid} successfully retrieved"
            user = format_db_item(user[0])
            result_dict["Item"] = user["AdvertIDs"]
            return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


# bu fonksiyon bir dictionary doner
# bu dictionary de "Status" islemin durumunu
# "Message" aciklamayi
# "Items" ise butun userlari bir dictionary listesi halinde doner. her user bir dictionary dir

def retrieve_all_users():

    try:
        TABLE_NAME = "FakeUser"
        select_statement = f"SELECT * FROM {TABLE_NAME}"
        response = client.execute_statement(Statement=select_statement)
        items = response["Items"]

        result_dict = {}
        users = []

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All users successfully retrieved"
        for item in items:
            tmp = format_db_item(item)
            users.append(tmp)

        result_dict["Items"] = users
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}




# UPDATE Functions

# butun normal attribute lar icin update fonksiyonlari olacak hem user hem de advert icin

# Ayrica user in liked films lerine film ekle veya liked films lerinden film cikar gibi fonksiyonlar da olacak

# Aybi sekilde watched films ve AdvertIDs icine bir seyler ekleme ve cikarma fonksiyonlari da olacak

# Ayrica advert in da attendeıds kismi icin update fonksiyonu olacak

# cikar kisimlari  delete functions bolomunde olacak

# bir update oldugu zaman hem user hem de advert de lastupdatedate current time ile guncellenecek


# DELETE Functions

# Normal attributelar icin delete fonksiyonu yazilmayacak

# dynamodb de olmayan bir item i silmeyece calistigimizda error vermiyor
# dolayısıyla for ile 1 den get_user_id veya get_advert_id ye kadar gecebiliriz




def delete_user(userid):
    # bu fonksiyon verilen userid ye sahip user i silecek

    # ayrica butun advert lara bakip eger advert in attendee id lerinde bu user varsa oradan da silinmeli

    # ayrica bu user in owner i oldugu butun ilanlar da silinmeli

    # 1) once o user in advertıds listesindeki butun advertlar silinmeli cunku bu user o advertlarin owner i ve artik sistemde bulunmayacak

    # 2) advertlar direk olarak silinebilir attendee ler ile ilgili bir sey yapmaya gerek yok. İlerde istenirse bu attendee lere bildirim vs atilabilir

    # 3) daha sonra o user silinecek


    pass

def delete_advert(advertid):

    # verilen id ye sahip butun advertlar silinecek

    # adverti silmeden once advertin owner ina gidilir ve onun advert ids kisimindan bu id cikartilir

    # daha sonra advert direk silinir

    pass


def delete_all_tables():
    
    # database de bulunan butun tablolari siler

    # bunu yapma yolu id_generator dan guncel user ve advert id leri alip for ile 1 den oraya kadar her biri icin silme requesti atilir

    # butun tablelar temizlendigi icin id_generator in initializeids fonksiyonu cagirilir
    
    pass

# ONEMLİ !!!!!   delete_all_users tarzinda bir fonksiyon yok cunku butun userlar silindigi zaman advertlar anlamsiz olur
#                dolayisiyla userlar silindigi zaman advertlarida silmek gerekir.


def delete_all_adverts():

    # bu fonksiyon butun advertlari siler ve butun userlarin advertids attributelarini bos liste yapar.

    # ayrica id_generator in initialize advert ids fonksiyonu kullanilarak advert id degeri initialize edilir

    pass



#response = client.get_item( # Now this table contains just dummy data
#    TableName='Student',
#    Key={
#        "StudentID":{
#            "N": "1"
#        }
#    })




# FakeUser tablosu  UserID partition key i type i number yine us east 1 icin yaratildi !!!
#
# FakeAdvert tablosu AdvertID partition key i type i number yine us east 1 icin yaratildi !!!
#
#


#test_statement = "SELECT * FROM FakeUser"    it works
 
#test_statement_2 = "SELECT * FROM FakeAdvert"  it works

#response = client.execute_statement(Statement=test_statement)  it works
 
#print(response)  it works

#response = client.execute_statement(Statement=test_statement_2) it works

#print(response)   it works

#statement = "SELECT * FROM Student WHERE StudentID=0" # IT WORKS !!!


def insert_user_values():

    values = []

    # "'UserID':1, 'CognitoAuthTokens':['access token of bkaslan','refresh token of bkaslan'], 'Name':'Berk', 'Surname':'Karaaslan', 'Username':'bkaslan', 'AdvertIDs': [1,3,7,8], 'Sex':'male', 'Email':'bkaslan@gmail.com', 'Age':22, 'Location':'Ankara-TUR', 'Bio':'This is a bio of bkaslan', 'ProfilePhoto': 'This is a string profile photo', 'LikedFilms':[100,400], 'WatchedFilms':[100,200,500,400], 'RegistrationDate':'2022-02-19 15:48:36.431698', 'LastLogIn':'2022-02-21 15:48:55.471318',  'LogInCount':10, 'Interests': ['Action', 'Thriller'], 'About':'This is an about section of bkaslan' ")                                                                           

    # calisiyorrr     values.append("'UserID': 1, 'CognitoAuthTokens': {'L':['access token of bkaslan','refresh token of bkaslan']}, 'Name': {'S':'Berk'}, 'Surname':{'S':'Karaaslan'}, 'Username':{'S':'bkaslan'}, 'AdvertIDs': {'L':[1,3,7,8]}, 'Sex':{'S':'male'}, 'Email':{'S':'bkaslan@gmail.com'}, 'Age':{'N':'22'}, 'Location':{'S':'Ankara-TUR'}, 'Bio':{'S':'This is a bio of bkaslan'}, 'ProfilePhoto': {'B':'This is a string profile photo'}, 'LikedFilms':{'L':[100,400]}, 'WatchedFilms':{'L':[100,200,500,400]}, 'RegistrationDate':{'S':'2022-02-19 15:48:36.431698'}, 'LastLogIn':{'S':'2022-02-21 15:48:55.471318'},  'LogInCount':{'N':'10'}, 'Interests': {'L':['Action', 'Thriller']}, 'About':{'S':'This is an about section of bkaslan'} ")                                                                           

    user1 = "'UserID': 1, 'CognitoAuthTokens': ['access token of bkaslan','refresh token of bkaslan'], 'Name': 'Berk', 'Surname':'Karaaslan', 'Username':'bkaslan', 'AdvertIDs':[1,3,7,8], 'Sex':'male', 'Email':'bkaslan@gmail.com', 'Age':22, 'Location':'Ankara-TUR', 'Bio':'This is a bio of bkaslan', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,400], 'WatchedFilms':[100,200,500,400], 'RegistrationDate':'2022-02-19 15:48:36.431698', 'LastLogIn':'2022-02-21 15:48:55.471318',  'LogInCount':10, 'Interests':['Action', 'Thriller'], 'About':'This is an about section of bkaslan' "                                                                        
    user2 = "'UserID': 2, 'CognitoAuthTokens': ['access token of sceran','refresh token of sceran'], 'Name': 'Suleyman', 'Surname':'Ceran', 'Username':'sceran', 'AdvertIDs':[], 'Sex':'male', 'Email':'sceran@gmail.com', 'Age':21, 'Location':'Ankara-TUR', 'Bio':'This is a bio of sceran', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,400,500], 'WatchedFilms':[300,500,600,100,400], 'RegistrationDate':'2022-01-01 12:35:45.000000', 'LastLogIn':'2022-05-15 23:59:58.171633',  'LogInCount':50, 'Interests':['Drama', 'Horror'], 'About':'This is an about section of sceran' "                                                                        
    user3 = "'UserID': 3, 'CognitoAuthTokens': ['access token of opolat','refresh token of opolat'], 'Name': 'Omer Faruk', 'Surname':'Polat', 'Username':'opolat', 'AdvertIDs':[6], 'Sex':'male', 'Email':'opolat@gmail.com', 'Age':22, 'Location':'Istanbul-TUR', 'Bio':'This is a bio of opolat', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[400,500,600], 'WatchedFilms':[100,200,300,400,500,600], 'RegistrationDate':'2022-11-27 01:00:17.000000', 'LastLogIn':'2022-11-30 14:20:03.171633',  'LogInCount':18, 'Interests':['Drama', 'Horror', 'Comedy'], 'About':'This is an about section of opolat'"
    user4 = "'UserID': 4, 'CognitoAuthTokens': ['access token of omujde','refresh token of omujde'], 'Name': 'Ozan', 'Surname':'Mujde', 'Username':'omujde', 'AdvertIDs':[], 'Sex':'male', 'Email':'omujde@gmail.com', 'Age':21, 'Location':'Izmir-TUR', 'Bio':'This is a bio of omujde', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100], 'WatchedFilms':[100,200,500], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':150, 'Interests':['Dark Humor', 'Horror'], 'About':'This is an about section of omujde'"
    user5 = "'UserID': 5, 'CognitoAuthTokens': ['access token of byalcin','refresh token of byalcin'], 'Name': 'Bugra', 'Surname':'Yalcin', 'Username':'byalcin', 'AdvertIDs':[], 'Sex':'male', 'Email':'byalcin@gmail.com', 'Age':20, 'Location':'Ankara-TUR', 'Bio':'This is a bio of byalcin', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[200], 'WatchedFilms':[100,180,200], 'RegistrationDate':'2022-07-06 03:47:59.161723', 'LastLogIn':'2022-07-06 03:47:59.161723',  'LogInCount':1, 'Interests':['Action', 'Comics'], 'About':'This is an about section of byalcin'"
    user6 = "'UserID': 6, 'CognitoAuthTokens': ['access token of cbloom','refresh token of cbloom'], 'Name': 'Casey', 'Surname':'Bloom', 'Username':'cbloom', 'AdvertIDs':[], 'Sex':'other', 'Email':'cbloom@gmail.com', 'Age':23, 'Location':'Berlin-GER', 'Bio':'This is a bio of cbloom', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[180,500], 'WatchedFilms':[180,100,300,500,400], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':61, 'Interests':['Horror', 'Anime'], 'About':'This is an about section of cbloom'"
    user7 = "'UserID': 7, 'CognitoAuthTokens': ['access token of mcartney','refresh token of mcartney'], 'Name': 'Monica', 'Surname':'Cartney', 'Username':'mcartney', 'AdvertIDs':[2,5], 'Sex':'female', 'Email':'mcartney@gmail.com', 'Age':20, 'Location':'Berlin-GER', 'Bio':'This is a bio of mcartney', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[150,100,500], 'WatchedFilms':[150,100,500], 'RegistrationDate':'2021-06-06 09:22:35.101220', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':12, 'Interests':['Drama', 'Biography'], 'About':'This is an about section of mcartney'"
    user8 = "'UserID': 8, 'CognitoAuthTokens': ['access token of dson','refresh token of dson'], 'Name': 'David', 'Surname':'Son', 'Username':'dson', 'AdvertIDs':[], 'Sex':'other', 'Email':'dson@gmail.com', 'Age':28, 'Location':'London-ENG', 'Bio':'This is a bio of dson', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[180,200], 'WatchedFilms':[180,200], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-01-31 23:44:12.131739',  'LogInCount':31, 'Interests':['Cartoon'], 'About':'This is an about section of dson'"
    user9 = "'UserID': 9, 'CognitoAuthTokens': ['access token of edoe','refresh token of edoe'], 'Name': 'Emma', 'Surname':'Doe', 'Username':'edoe', 'AdvertIDs':[], 'Sex':'female', 'Email':'edoe@gmail.com', 'Age':19, 'Location':'London-ENG', 'Bio':'This is a bio of edoe', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[200,400], 'WatchedFilms':[200,100,300,500,400], 'RegistrationDate':'2019-06-08 12:31:33.343536', 'LastLogIn':'2021-11-30 18:03:21.180321',  'LogInCount':72, 'Interests':['Dc', 'Marvel'], 'About':'This is an about section of edoe'"
    user10 = "'UserID': 10, 'CognitoAuthTokens': ['access token of jdoe','refresh token of jdoe'], 'Name': 'James', 'Surname':'Doe', 'Username':'jdoe', 'AdvertIDs':[4], 'Sex':'male', 'Email':'jdoe@gmail.com', 'Age':24, 'Location':'London-ENG', 'Bio':'This is a bio of jdoe', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,150,200,400], 'WatchedFilms':[180,150,100,300,500,400], 'RegistrationDate':'2019-06-08 12:31:33.343536', 'LastLogIn':'2021-11-30 18:03:21.180321',  'LogInCount':60, 'Interests':['Civil War', 'Cold War'], 'About':'This is an about section of jdoe'"


    # bu sekilde her useri ekle !!!



    values.append(user1)
    values.append(user2)
    values.append(user3)
    values.append(user4)
    values.append(user5)
    values.append(user6)
    values.append(user7)
    values.append(user8)
    values.append(user9)
    values.append(user10)





    # 400 kilobaytin altindaki stringler tabloya koyulabiliyor. profile fotosu string olarak tutulacak.

    # Profile fotosu string olarak kaydediliyor. onu string olarak kaydet ve alinca image e donusumu yap

    # 




    #values.append("'UserID': {'N':'1'}, 'CognitoAuthTokens': {'L':['access token of bkaslan','refresh token of bkaslan']}, 'Name': {'S':'Berk'}, 'Surname':{'S':'Karaaslan'}, 'Username':{'S':'bkaslan'}, 'AdvertIDs': {'L':[1,3,7,8]}, 'Sex':{'S':'male'}, 'Email':{'S':'bkaslan@gmail.com'}, 'Age':{'N':'22'}, 'Location':{'S':'Ankara-TUR'}, 'Bio':{'S':'This is a bio of bkaslan'}, 'ProfilePhoto': {'B':'This is a string profile photo'}, 'LikedFilms':{'L':[100,400]}, 'WatchedFilms':{'L':[100,200,500,400]}, 'RegistrationDate':{'S':'2022-02-19 15:48:36.431698'}, 'LastLogIn':{'S':'2022-02-21 15:48:55.471318'},  'LogInCount':{'N':'10'}, 'Interests': {'L':['Action', 'Thriller']}, 'About':{'S':'This is an about section of bkaslan'} ")                                                                           

    insert_statement = "INSERT INTO FakeUser VALUE {" + values[0] + "}"

    select_statement = "SELECT * FROM FakeUser"

    delete_statement = "DELETE FROM FakeUser WHERE UserID=1"


    for i in range(10):
        temp_statement = "INSERT INTO FakeUser VALUE {" + values[i] + "}"
        response = client.execute_statement(Statement=temp_statement) 

    #response = client.execute_statement(Statement=delete_statement) 

    response = client.execute_statement(Statement=select_statement) 

    print(response["Items"])



#insert_user_values()


def insert_advert_values():

    values = []

                                                                             

    advert1 = "'AdvertID': 1, 'OwnerID': 1, 'Date': '2022-02-20 20:30:00.000000', 'RegistrationDate':'2022-02-14 19:47:16.001234', 'LastUpdateDate':'2022-02-14 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,3,4,5], 'Status': 'Active', 'FilmID': 100 "                                                                        
    advert2 = "'AdvertID': 2, 'OwnerID': 7, 'Date': '2022-02-20 20:30:00.000000', 'RegistrationDate':'2022-02-16 19:47:16.001234', 'LastUpdateDate':'2022-02-16 19:47:16.001234', 'Quota': 2, 'AttendeePreference':'male', 'AttendeeIDs': [7,10], 'Status': 'Active', 'FilmID': 150 "
    advert3 = "'AdvertID': 3, 'OwnerID': 1, 'Date': '2022-02-25 21:00:00.000000', 'RegistrationDate':'2022-02-12 20:33:16.001234', 'LastUpdateDate':'2022-02-12 20:47:16.172144', 'Quota': 3, 'AttendeePreference':'female', 'AttendeeIDs': [1,7,9], 'Status': 'Active', 'FilmID': 200 "
    advert4 = "'AdvertID': 4, 'OwnerID': 10, 'Date': '2022-02-28 12:30:00.000000', 'RegistrationDate':'2022-02-15 10:09:16.001234', 'LastUpdateDate':'2022-02-15 11:37:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [10,5,6,7,8], 'Status': 'Active', 'FilmID': 180 "
    advert5 = "'AdvertID': 5, 'OwnerID': 7, 'Date': '2022-02-25 11:00:00.000000', 'RegistrationDate':'2022-02-14 19:47:16.001234', 'LastUpdateDate':'2022-02-15 20:55:18.123456', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [7,2,9,16], 'Status': 'Active', 'FilmID': 100 "
    advert6 = "'AdvertID': 6, 'OwnerID': 3, 'Date': '2021-05-25 23:00:00.000000', 'RegistrationDate':'2021-05-10 19:47:16.001234', 'LastUpdateDate':'2021-05-10 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [3,2,9,10,6], 'Status': 'Previous', 'FilmID': 300 "
    advert7 = "'AdvertID': 7, 'OwnerID': 1, 'Date': '2021-01-13 15:30:00.000000', 'RegistrationDate':'2022-01-06 19:47:16.001234', 'LastUpdateDate':'2022-01-06 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,9,10,6], 'Status': 'Previous', 'FilmID': 500 "
    advert8 = "'AdvertID': 8, 'OwnerID': 1, 'Date': '2021-02-14 20:00:00.000000', 'RegistrationDate':'2021-02-03 12:33:21.124346', 'LastUpdateDate':'2021-02-03 12:33:21.124346', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,9,10,6], 'Status': 'Previous', 'FilmID': 400 "


   



    values.append(advert1)
    values.append(advert2)
    values.append(advert3)
    values.append(advert4)
    values.append(advert5)
    values.append(advert6)
    values.append(advert7)
    values.append(advert8)
    
  





    # 400 kilobaytin altindaki stringler tabloya koyulabiliyor. profile fotosu string olarak tutulacak.

    # Profile fotosu string olarak kaydediliyor. onu string olarak kaydet ve alinca image e donusumu yap

    # 




    #values.append("'UserID': {'N':'1'}, 'CognitoAuthTokens': {'L':['access token of bkaslan','refresh token of bkaslan']}, 'Name': {'S':'Berk'}, 'Surname':{'S':'Karaaslan'}, 'Username':{'S':'bkaslan'}, 'AdvertIDs': {'L':[1,3,7,8]}, 'Sex':{'S':'male'}, 'Email':{'S':'bkaslan@gmail.com'}, 'Age':{'N':'22'}, 'Location':{'S':'Ankara-TUR'}, 'Bio':{'S':'This is a bio of bkaslan'}, 'ProfilePhoto': {'B':'This is a string profile photo'}, 'LikedFilms':{'L':[100,400]}, 'WatchedFilms':{'L':[100,200,500,400]}, 'RegistrationDate':{'S':'2022-02-19 15:48:36.431698'}, 'LastLogIn':{'S':'2022-02-21 15:48:55.471318'},  'LogInCount':{'N':'10'}, 'Interests': {'L':['Action', 'Thriller']}, 'About':{'S':'This is an about section of bkaslan'} ")                                                                           

    insert_statement = "INSERT INTO FakeAdvert VALUE {" + values[0] + "}"

    select_statement = "SELECT * FROM FakeAdvert"

    delete_statement = "DELETE FROM FakeAdvert WHERE UserID=1"


    #for i in range(8):
    #    temp_statement = "INSERT INTO FakeAdvert VALUE {" + values[i] + "}"
    #    response = client.execute_statement(Statement=temp_statement) 

    #response = client.execute_statement(Statement=delete_statement) 

    response = client.execute_statement(Statement=select_statement) 

    print(response["Items"])


    


#insert_advert_values()










def insert_sample_user():

    statement = "INSERT INTO FakeUser VALUE {" + "'UserID': 100, 'FavoriteFood':'Ice Cream'" + "}"
    client.execute_statement(Statement=statement) 
    select_statement = "SELECT * FROM FakeUser WHERE UserID=100"
    response = client.execute_statement(Statement=select_statement) 

    print(response["Items"][0]["FavoriteFood"]["S"])


    
    


#insert_sample_user()







# bir tane dummy user ekle ve bu user i geri cagir select ile
# donen itemlerden istenen dictionary yi alma yontemi

# [d for d in a if d['name'] == 'pluto']
# burada a dedigimiz dictionary listesi
# d ise tek dictionary yi listeye eklemek icin tmp variable
# eger name attribute u pluto ise onu aliyor.





statement = "SELECT * FROM Student" # IT WORKS !!!

item = (2, 'Berk', 'Karaaslan', 20)

statement2 = "INSERT INTO Student VALUE {'StudentID':2,'Name':'Berk', 'Surname':'Karaaslan','Age':20}" # It works !!!  This statement adds a new student to student table

# statement2 ile Student tablosuna yeni bir entry ekledik 

statement3 = "UPDATE Student SET Name='NotBerk' SET NewAttribute=10 WHERE Name='Berk' AND StudentID=2" # It works !!!  WHERE kisminda her key icin bir condition olmak zorunda eger studentıd kismi kaldirilirsa calismiyor

# statement3 ile adi Berk ve ID si 2 olan kullanicinin adini NotBerk yaptik ve ona yeni bir attribute ekledik
# evet sorgunun icinde yeni bir attribute eklenebiliyor.
# link: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.update.html
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.delete.html

statement4 = "UPDATE Student SET Name='Berk' SET NewAttribute=10 WHERE Name='NotBerk' AND StudentID=2 OR StudentID!=2"

#statement4 = "UPDATE Student SET Name='Berk' SET NewAttribute=10 WHERE Name='NotBerk' AND StudentID IN (SELECT StudentID FROM Student)"

statement5 = "SELECT StudentID FROM Student"

statement6 = "UPDATE Student REMOVE Name WHERE Name='NotBerk' AND StudentID=2" # It works !!! Bu statement ıd si 2 olan ve adi NotBerk olan satirdan "Name" attribute unu sildi
# bir list veya set tarzi bir attribute un icinde belirli bir elemani silmeye calis


# COK ONEMLI  !!!!   Burada Update ve remove islemlerinde where conditionı olarak mutlaka butun key attributelara bir deger girilmek zorunda
# Yani bir key attribute un degeri bos birakilarak update ve remove yapilamaz ancak select ve bir attribute icin remove yapilabilir 
# Insert statement ı normal bir sekilde yapilabilir onun icin ozel bir seye gerek yoktur.

#response = client.execute_statement(Statement=statement) 

#my_key_list = response["Items"]

#my_keys = []

#for i in my_key_list:
#    my_keys.append(*i.values())

#my_real_keys = []

#for i in my_keys:
#    my_real_keys.append(*i.values())

#print(set(my_real_keys))    

#response = client.execute_statement(Statement=statement4)


# This response contains 2 part of information. "Item" and "ResponseMetadata"
# "Item" is the meaningful part for us
# We can use "Item" part like a json object. 

#for i in response:
#    print(i,"->", response[i])

#meaningful_item = response["Items"] # It is a dictionary object, we can print all key-value pairs in this dictionary
#Note: This dictionary's values are dictionary too. 

#print(response["Items"])  

#print(meaningful_item)

#Surname {'S': 'Doe'}
#Age {'N': '20'}
#StudentID {'N': '1'}
#Name {'S': 'John'}

# Below lines are examples of meaningful_item's key-value pairs
# Keys of this dictionaries are Attribute Type, ex: 'S' means String
# Values of this dictionaries are actual values that comes from DynamoDB

#for item in meaningful_item:
#    print(item, meaningful_item[item])