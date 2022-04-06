import boto3
from current_time import *

INITIAL_LOGIN_VALUE = 1 # Login count bunu tutacak
INITIAL_ID_VALUE = 1

AWS_ACCESS_KEY_ID = "AKIASCXGL6JSX2WDYG4Z"
AWS_SECRET_ACCESS_KEY = "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"
DEFAULT_REGION = "us-east-1" # AWS wants a region. In my case it is "us-east-1"

client = boto3.client('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = DEFAULT_REGION)

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


def get_user_id(): # This function returns current user id. We can use this id when creating a user.
    
    TABLE_NAME = "IDs"
    select_statement = f"SELECT * FROM {TABLE_NAME} WHERE Name='UserID'"
    response = client.execute_statement(Statement=select_statement)
    userid_dict = response["Items"]
    userid_dict = format_db_item(userid_dict[0])
    UserID = userid_dict["Value"]
    return UserID
    
def increment_user_id(): # This function increments user id. We MUST use this function after we call get_user_id function to ensure that our user id is up to date
    
    UserID = get_user_id()
    UserID = UserID + 1
    update_statement = f"UPDATE \"IDs\" SET \"Value\"={UserID} WHERE \"Name\"='UserID'"
    response = client.execute_statement(Statement=update_statement)

def get_advert_id(): # This function returns current advert id. We can use this id when creating an advert.
    TABLE_NAME = "IDs"
    select_statement = f"SELECT * FROM {TABLE_NAME} WHERE Name='AdvertID'"
    response = client.execute_statement(Statement=select_statement)
    advertid_dict = response["Items"]
    advertid_dict = format_db_item(advertid_dict[0])
    AdvertID = advertid_dict["Value"]
    return AdvertID

def increment_advert_id(): # This function increments advert id. We MUST use this function after we call get_advert_id function to ensure that our advert id is up to date
    
    AdvertID = get_advert_id()
    AdvertID = AdvertID + 1
    update_statement = f"UPDATE \"IDs\" SET \"Value\"={AdvertID} WHERE \"Name\"='AdvertID'"
    response = client.execute_statement(Statement=update_statement)

def initialize_user_id(): # This function initializes user id with initial value which is 1

    UserID = INITIAL_ID_VALUE
    update_statement = f"UPDATE \"IDs\" SET \"Value\"={UserID} WHERE \"Name\"='UserID'"
    response = client.execute_statement(Statement=update_statement)

def initialize_advert_id(): # This function initializes advert id with initial value which is 1
    
    AdvertID = INITIAL_ID_VALUE
    update_statement = f"UPDATE \"IDs\" SET \"Value\"={AdvertID} WHERE \"Name\"='AdvertID'"
    response = client.execute_statement(Statement=update_statement)


def initialize_ids(): # This function initializes both user id and advert id with initial value which is 1
    
    initialize_user_id()
    initialize_advert_id()

# SADECE email zorunlu arguman diger butun argumanlar opsiyonel
def create_user(email,authtokens=None,name=None,surname=None,username=None,sex=None,age=None,location=None,bio=None,profilephoto=None,likedfilms=None,interests=None,about=None):
    
    # email disinda hepsi opsiyonel parametre
    
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
        
        item = ""

        user_id = get_user_id()
        increment_user_id()
        advert_ids = [] # Initially an empty list
        watched_films = []
        attended_adverts = []
        registration_date = "'" + curr_time() + "'"
        last_log_in = registration_date # Initially they are equal
        log_in_count = INITIAL_LOGIN_VALUE
        last_update_date = registration_date # Initially they are equal
        formatted_email = "'" + email + "'"

        item = item = f"'UserID': {user_id}, 'AdvertIDs': {advert_ids}, 'Email': {formatted_email}, 'WatchedFilms': {watched_films}, 'RegistrationDate': {registration_date}, 'LastLogIn': {last_log_in},  'LogInCount': {log_in_count}, 'LastUpdateDate': {last_update_date}, 'AttendedAdverts': {attended_adverts}"

        if name is not None:
            formatted_name = "'" + name + "'"
            item = item + f", 'Name':{formatted_name}"

        if surname is not None:
            formatted_surname = "'" + surname + "'"
            item = item + f", 'Surname':{formatted_surname}"

        if username is not None:
            formatted_username = "'" + username + "'"
            item = item + f", 'Username':{formatted_username}"

        if sex is not None:
            formatted_sex = "'" + sex + "'"
            item = item + f", 'Sex':{formatted_sex}"

        if age is not None:
            age = int(age)
            item = item + f", 'Age':{age}"

        if location is not None:
            formatted_location = "'" + location + "'"
            item = item + f", 'Location':{formatted_location}"

        if bio is not None:
            formatted_bio = "'" + bio + "'"
            item = item + f", 'Bio':{formatted_bio}"

        if profilephoto is not None:
            formatted_photo = "'" + profilephoto + "'"
            item = item + f", 'ProfilePhoto':{formatted_photo}"

        if about is not None:
            formatted_about = "'" + about + "'"
            item = item + f", 'About':{formatted_about}"

        if authtokens is not None:
            item = item + f", 'CognitoAuthTokens':{authtokens}"

        if likedfilms is not None:
            item = item + f", 'LikedFilms':{likedfilms}"

        if interests is not None:
            item = item + f", 'Interests':{interests}"

        
        TABLE_NAME = 'FakeUser'
        insert_statement = f"INSERT INTO {TABLE_NAME} VALUE " + "{" + item + "}"
        result_dict = {} # bunun icine status, message gibi attribute lar koy.
        # user ıd vs de bunun icinde donulecek
        response = client.execute_statement(Statement=insert_statement) 
        #response["Items"]  normalde birsey donmemesi lazim

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"New user successfully created with user id:{user_id}"
        result_dict["UserID"] = user_id
        return result_dict

    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    

def retrieve_user(userid):
    # PARAMETER TYPES

    # userid -> int

    try:
        userid = int(userid) # type casting gerekli !
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


def validate_tokens(userid,tokens): 
    # PARAMETER TYPES

    # userid -> int
    # tokens -> str list


    # userid si verilen useri getirir ve userin tokenlarini parametre olarak verilen tokenlarla karsilastirir
    # bu fonksiyonun dogru calismasi icin tokenlarin sirasinin tablodaki ile ayni olması gerekir. 
    # eger bu ozellik saglanamayacaksa bu implementation degistirilmelidir.

    # eger tokenlar tablodaki ile ayni ise true aksi halde false doner

    user_query = retrieve_user(userid)

    if user_query["Status"] == "Fail": # eger fail etti ise false don
        return False

    user = user_query["Item"]
    user_auth_tokens = user["CognitoAuthTokens"]

    if user_auth_tokens == tokens:
        return True
    else:
        return False
    



def retrieve_advert(advertid):
    # PARAMETER TYPES

    # advertid -> int
    try:
        advertid = int(advertid)
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


def retrieve_users_all_adverts(userid):
    # PARAMETER TYPES

    # userid -> int
    try:
        userid = int(userid)
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


def retrieve_user_with_email(email): # email unique oldugu icin verilen email e sahip user i donecek
    # PARAMETER TYPES

    # email -> str

    try:

        user_query = retrieve_all_users()
        result_dict = {}
        if user_query["Status"] == "Fail": # fail etti
            result_dict["Status"] = user_query["Status"]
            result_dict["Message"] = user_query["Message"]
            return result_dict

        users = user_query["Items"]
        for user in users:
            if user["Email"] == email: # bu user donulecek
                result_dict["Status"] = "Success"
                result_dict["Message"] = f"User with email:{email} is successfully retrieved"
                result_dict["Item"] = user
                return result_dict
            
        result_dict["Status"] = "Fail"
        result_dict["Message"] = f"No such user exist with email:{email}"
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def retrieve_all_users_with_name_and_surname(name=None,surname=None): # verilenleri dahil edecek
    # PARAMETER TYPES

    # name -> str (optional)
    # surname -> str (optional)

    try:

        result_dict = {}
        if name is None and surname is None: # eger parametre verilmedi ise
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"You must specify at least one of name and surname"
            return result_dict

        users_query = retrieve_all_users()
        if users_query["Status"] == "Fail": # islem basarisiz
            result_dict["Status"] = users_query["Status"]
            result_dict["Message"] = users_query["Message"]
            return result_dict

        users = users_query["Items"]
        users_with_name_and_surname = [] # name veya surname i iceren userlar

        for user in users:
            if name is None: # name None ise surname kesinlikle None degildir cunku oldugu senaryoyu kontrol ettik.
                if user["Surname"] == surname: # name None oldugu icin eger Surname i ayni ise direk ekledik
                    users_with_name_and_surname.append(user)
                
            else: # name None degil 
                if surname is None: # surname None dolayisiyla sadece name e bakicaz
                    if user["Name"] == name:
                        users_with_name_and_surname.append(user)
                
                else: # burada hem name hem surname e bakicaz cunku ikiside None degil
                    if user["Name"] == name and user["Surname"] == surname:
                        users_with_name_and_surname.append(user)

        if name is None:
            formatted_name = 'None'
        else:
            formatted_name = name

        if surname is None:
            formatted_surname = 'None'
        else:
            formatted_surname = surname

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All users with name:{formatted_name} and surname:{formatted_surname} successfully retrieved"
        result_dict["Items"] = users_with_name_and_surname
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def retrieve_all_adverts():

    try:
        TABLE_NAME = "FakeAdvert"
        select_statement = f"SELECT * FROM {TABLE_NAME}"
        response = client.execute_statement(Statement=select_statement)
        items = response["Items"]

        result_dict = {}
        adverts = []

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All adverts successfully retrieved"
        for item in items:
            tmp = format_db_item(item)
            adverts.append(tmp)

        result_dict["Items"] = adverts
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def retrieve_all_adverts_with_filmid(filmid): # verilen filmid ye sahip butun ilanlari donecek
    # PARAMETER TYPES

    # filmid -> int

    try:

        filmid = int(filmid) # parametre cast gereklidir
        result_dict = {}
        adverts_query = retrieve_all_adverts()
        if adverts_query["Status"] == "Fail": # islem basarisiz
            result_dict["Status"] = adverts_query["Status"]
            result_dict["Message"] = adverts_query["Message"]
            result_dict["FilmID"] = filmid
            return result_dict

        adverts = adverts_query["Items"]
        adverts_with_filmid = [] # filmid yi iceren advertlar

        for advert in adverts:
            if advert["FilmID"] == filmid: # eger id si ayni ise donecegimiz listeye adverti ekle
                adverts_with_filmid.append(advert)

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All adverts with filmid:{filmid} successfully retrieved"
        result_dict["Items"] = adverts_with_filmid
        return result_dict
        
    except:
        return {"Status":"Fail", "Message": "An exception occured"}


# bu fonksiyon user in "UserID", "AdvertIDs", "LikedFilms", "WatchedFilms" disinda kalan butun attribute larini update eder.
# burada belirtilen attribute lari da update edebilir ancak direk uzerine yazar yani ilan listesine eleman ekle eleman cikar gibi seyleri yapamaz!
# bu islemleri 1 asagidaki fonksiyon yapacak
# attribute parametresi guncellenecek attribute un ismini icerir
# new_value ise bu attribute un alacagi degeri tasir

def update_user(userid, attribute, new_value): # verilen user i verilen attribute ismini new value ile update edecek
    # PARAMETER TYPES

    # userid -> int
    # attribute -> str
    # new_value -> it could be any valid attribute type
    
    try:
        TABLE_NAME = "FakeUser"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE UserID={userid}"
        response = client.execute_statement(Statement=select_statement)
        user = response["Items"]
        result_dict = {}

        # LogInCount a bakilmadi !!!!!!!!
        if attribute == "Age": # parametre cast gereklidir !
            new_value = int(new_value)

        if len(user) == 0: # No such user exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such user exist with user id:{userid}"
            result_dict["UserID"] = userid
            return result_dict
        else: # User exist
          
            old = None
            user = format_db_item(user[0])
            last_update_date = "'" + curr_time() + "'" # user update edildigi icin son guncellenme tarihi guncellenecek
            
            if attribute in user.keys(): # we must get the old value
                old = user[attribute]
            
            result_dict["NewValue"] = new_value # onceden ekleniyor cunku str formatlayinca basina ve sonuna tirnak geliyor
            if type(new_value) is str: # deger str olunca tirnak isaretinden dolayi koymazsak kiziyor
                new_value = "'" + new_value + "'"

            update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={new_value} SET LastUpdateDate={last_update_date} WHERE UserID={userid}"
            response = client.execute_statement(Statement=update_statement)

            result_dict["Status"] = "Success"
            if old is None: # eskiden bu attribute yokmus
                result_dict["Message"] = f"Attribute with attribute name:{attribute} has successfully added to user with user id:{userid}"
            else:
                result_dict["Message"] = f"Attribute with attribute name:{attribute} has successfully updated for user with user id:{userid}"

            result_dict["UserID"] = userid
            if old is not None:
                result_dict["OldValue"] = old # eger old valuesu varsa ekleriz
            #result_dict["NewValue"] = new_value
            return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}



# "AdvertIDs", "LikedFilms", "WatchedFilms"
def update_user_list_attributes(userid, attribute, value, op_type):
    # PARAMETER TYPES

    # userid -> int
    # attribute -> str
    # value -> it could be any valid attribute type
    # op_type -> str  only valid values are "add" and "remove" !


    # attribute str olarak hangi parametrenin update edilecegini tutacak
    # value herhangi bir type da add veya remove yapilacak item i tutacak
    # op_type ise string olarak "add" veya "remove" degerlerini alabilecek

    try:
        TABLE_NAME = "FakeUser"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE UserID={userid}"
        response = client.execute_statement(Statement=select_statement)
        user = response["Items"]
        result_dict = {}

        if attribute == "LikedFilms": # Yeni list attribute lar gelirse onlarin da kontrol edilmesi gerekir.
            value = int(value)
        elif attribute == "WatchedFilms":
            value = int(value)
        elif attribute == "AttendedAdverts":
            value = int(value)
        elif attribute == "AdvertIDs":
            value = int(value)

        if len(user) == 0: # No such user exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such user exist with user id:{userid}"
            result_dict["UserID"] = userid
            return result_dict
        else: # User exist
            
                user = format_db_item(user[0])
                last_update_date = "'" + curr_time() + "'" # user update edildigi icin son guncellenme tarihi guncellenecek
                
                if op_type == "add":

                    if attribute not in user.keys(): # boyle bir attribute yok

                        list_attribute = []
                        list_attribute.append(value)
                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE UserID={userid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} has successfully added to user:{userid} with value:{value}"
                        result_dict["UserID"] = userid
                        return result_dict

                    list_attribute = user[attribute] # ekleme yapilacak attribute u al

                    if value in list_attribute: # deger zaten varmis tekrar ekleme yapilmayacak uygun bir mesajla don

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} is already contains value:{value}"
                        result_dict["UserID"] = userid
                        return result_dict

                    else: # deger yokmus simdi eklenecek

                        list_attribute.append(value) # value yu attribute a ekle

                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE UserID={userid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Value:{value} is successfully added to attribute:{attribute}"
                        result_dict["UserID"] = userid
                        return result_dict

                elif op_type == "remove": # silinecek



                    if attribute not in user.keys(): # boyle bir attribute yok

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"User with user id:{userid} already does not contain attribute:{attribute}"
                        result_dict["UserID"] = userid
                        return result_dict

                    list_attribute = user[attribute] # silme yapilacak attribute u al

                    if value in list_attribute: # deger varmis silinmesi gerekir

                        list_attribute.remove(value) # degeri attribute dan sil

                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE UserID={userid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Value:{value} is successfully deleted from attribute:{attribute}"
                        result_dict["UserID"] = userid
                        return result_dict

                    else: # deger yokmus bir sey yapmaya gerek yok

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} does not contain value:{value}"
                        result_dict["UserID"] = userid
                        return result_dict

                else:
                    result_dict["Status"] = "Fail"
                    result_dict["Message"] = "Bad op_type. Valid values for op_type are \"add\" and \"remove\""
                    return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def update_advert(advertid, attribute, new_value): # verilen user i verilen attribute ismini new value ile update edecek
    # PARAMETER TYPES

    # advertid -> int
    # attribute -> str
    # new_value -> it could be any valid attribute type
    
    try:
        TABLE_NAME = "FakeAdvert"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE AdvertID={advertid}"
        response = client.execute_statement(Statement=select_statement)
        advert = response["Items"]
        result_dict = {}

        if attribute == "FilmID": # Baska int tipinde attribute eklenirse bu islem gereklidir !
            new_value = int(new_value)
        elif attribute == "OwnerID":
            new_value = int(new_value)
        elif attribute == "Quota":
            new_value = int(new_value)
        

        if len(advert) == 0: # No such advert exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such advert exist with advert id:{advertid}"
            result_dict["AdvertID"] = advertid
            return result_dict
        else: # Advert exist
          
            old = None
            advert = format_db_item(advert[0])
            last_update_date = "'" + curr_time() + "'" # advert update edildigi icin son guncellenme tarihi guncellenecek
            
            if attribute in advert.keys(): # we must get the old value
                old = advert[attribute]
            
            result_dict["NewValue"] = new_value
            if type(new_value) is str: # deger str olunca tirnak isaretinden dolayi koymazsak kiziyor
                new_value = "'" + new_value + "'"

            update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={new_value} SET LastUpdateDate={last_update_date} WHERE AdvertID={advertid}"
            response = client.execute_statement(Statement=update_statement)

            result_dict["Status"] = "Success"
            if old is None: # eskiden bu attribute yokmus
                result_dict["Message"] = f"Attribute with attribute name:{attribute} has successfully added to advert with advert id:{advertid}"
            else:
                result_dict["Message"] = f"Attribute with attribute name:{attribute} has successfully updated for advert with advert id:{advertid}"

            result_dict["AdvertID"] = advertid
            if old is not None:
                result_dict["OldValue"] = old # eger old valuesu varsa ekleriz
            #result_dict["NewValue"] = new_value
            return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def update_advert_list_attributes(advertid, attribute, value, op_type):
    # PARAMETER TYPES

    # advertid -> int
    # attribute -> str
    # value -> it could be any valid attribute type
    # op_type -> str  only valid values are "add" and "remove" !

    # attribute str olarak hangi parametrenin update edilecegini tutacak
    # value herhangi bir type da add veya remove yapilacak item i tutacak
    # op_type ise string olarak "add" veya "remove" degerlerini alabilecek

    try:
        # update fonksiyonlarinda disardan parametre gelince string gibi davraniyor 
        # gelebilecek parametreleri kontrol et ve type cast yap
        # advertin list attribute u attendeeIDs ve pending requests var
        TABLE_NAME = "FakeAdvert"
        select_statement = f"SELECT * FROM {TABLE_NAME} WHERE AdvertID={advertid}"
        response = client.execute_statement(Statement=select_statement)
        advert = response["Items"]
        result_dict = {}

        if attribute == "AttendeeIDs": # Yeni list attribute lar gelirse onlarin da kontrol edilmesi gerekir.
            value = int(value)
        elif attribute == "PendingRequests":
            value = int(value)

        if len(advert) == 0: # No such advert exist
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"No such advert exist with advert id:{advertid}"
            result_dict["AdvertID"] = advertid
            return result_dict
        else: # Advert exist
            
                advert = format_db_item(advert[0])
                last_update_date = "'" + curr_time() + "'" # advert update edildigi icin son guncellenme tarihi guncellenecek
                
                if op_type == "add":

                    if attribute not in advert.keys(): # boyle bir attribute yok

                        list_attribute = []
                        list_attribute.append(value)
                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE AdvertID={advertid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} has successfully added to advert:{advertid} with value:{value}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                    list_attribute = advert[attribute] # ekleme yapilacak attribute u al

                    if value in list_attribute: # deger zaten varmis tekrar ekleme yapilmayacak uygun bir mesajla don

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} is already contains value:{value}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                    else: # deger yokmus simdi eklenecek

                        list_attribute.append(value) # value yu attribute a ekle

                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE AdvertID={advertid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Value:{value} is successfully added to attribute:{attribute}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                elif op_type == "remove": # silinecek



                    if attribute not in advert.keys(): # boyle bir attribute yok

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Advert with advert id:{advertid} already does not contain attribute:{attribute}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                    list_attribute = advert[attribute] # silme yapilacak attribute u al

                    if value in list_attribute: # deger varmis silinmesi gerekir

                        list_attribute.remove(value) # degeri attribute dan sil

                        update_statement = f"UPDATE {TABLE_NAME} SET {attribute}={list_attribute} SET LastUpdateDate={last_update_date} WHERE AdvertID={advertid}"
                        response = client.execute_statement(Statement=update_statement)

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Value:{value} is successfully deleted from attribute:{attribute}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                    else: # deger yokmus bir sey yapmaya gerek yok

                        result_dict["Status"] = "Success"
                        result_dict["Message"] = f"Attribute:{attribute} does not contain value:{value}"
                        result_dict["AdvertID"] = advertid
                        return result_dict

                else:
                    result_dict["Status"] = "Fail"
                    result_dict["Message"] = "Bad op_type. Valid values for op_type are \"add\" and \"remove\""
                    return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}




# Dikkat !!!
# Asagidaki fonksiyonlar ilanlarin "PendingRequests" attribute u olmadiginda duzgun calismayabilir !!!!!

def join_advert(advertid,userid): # verilen user i verilen advert in pending requests ine eger orada ekli degilse ekleyecek
    return update_advert_list_attributes(int(advertid),"PendingRequests",int(userid),"add")

def accept_user(advertid,userid): #verilen advert icin userid yi pending requests den cikar ve attendeeids e ekle

    try:
        
        result_dict = {}
        remove_query = update_advert_list_attributes(int(advertid),"PendingRequests",int(userid),"remove")
        if remove_query["Status"] == "Fail": # eger silemedi ise ya boyle bir ilan yok ya op_type yanlis yada bir exception oldu
            result_dict["Status"] = remove_query["Status"]
            result_dict["Message"] = remove_query["Message"]
            return result_dict

        add_query = update_advert_list_attributes(int(advertid),"AttendeeIDs",int(userid),"add")
        if add_query["Status"] == "Fail": # eger ekleyemedi ise ya boyle bir ilan yok ya op_type yanlis yada bir exception oldu
            result_dict["Status"] = add_query["Status"]
            result_dict["Message"] = add_query["Message"]
            return result_dict

        user_update_query = update_user_list_attributes(int(userid),"AttendedAdverts",int(advertid),"add") # bu user in attendedadverts ina ilani ekleriz
        if user_update_query["Status"] == "Fail":
            result_dict["Status"] = user_update_query["Status"]
            result_dict["Message"] = user_update_query["Message"]
            return result_dict
        
        result_dict["Status"] = "Success"
        result_dict["Message"] = f"User with userid:{userid} is successfully accepted to advert with advertid:{advertid}"
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


def reject_user(advertid,userid): # verilen advert icin user id yi pending requests den sil
    
    try:

        result_dict = {}
        remove_query = update_advert_list_attributes(int(advertid),"PendingRequests",int(userid),"remove")
        if remove_query["Status"] == "Fail": # eger silemedi ise ya boyle bir ilan yok ya op_type yanlis yada bir exception oldu
            result_dict["Status"] = remove_query["Status"]
            result_dict["Message"] = remove_query["Message"]
            return result_dict

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"User with userid:{userid} is successfully rejected to advert with advertid:{advertid}"
        return result_dict

    except:
        return {"Status":"Fail", "Message": "An exception occured"}



def create_advert(ownerid,date,quota,preference,filmid,description):
    # PARAMETER TYPES

    # ownerid -> int
    # date -> str
    # quota -> int
    # preference -> str
    # filmid -> int
    # description -> str

    try: 

        ownerid = int(ownerid) # parametre cast gereklidir !
        quota = int(quota)
        filmid = int(filmid)

        advert_id = get_advert_id()
        increment_advert_id()
        registration_date = "'" + curr_time() + "'"
        formatted_date = "'" + date + "'"
        formatted_preference = "'" + preference + "'"
        formatted_description = "'" + description + "'"
        last_update_date = registration_date # Initially they are equal
        attendee_ids = []
        pending_requests = []
        attendee_ids.append(ownerid)
        status = "'Active'"

        TABLE_NAME = 'FakeAdvert'
        item = f"'AdvertID': {advert_id}, 'OwnerID': {ownerid}, 'Description': {formatted_description}, 'Date': {formatted_date}, 'RegistrationDate': {registration_date}, 'LastUpdateDate': {last_update_date}, 'Quota': {quota}, 'AttendeePreference': {formatted_preference}, 'AttendeeIDs': {attendee_ids}, 'Status': {status}, 'FilmID': {filmid}, 'PendingRequests': {pending_requests}"
        insert_statement = f"INSERT INTO {TABLE_NAME} VALUE " + "{" + item + "}"

        result_dict = {} 

        response = client.execute_statement(Statement=insert_statement) 
        #response["Items"]  normalde birsey donmemesi lazim
        user_response = update_user_list_attributes(ownerid,"AdvertIDs",advert_id,"add") # bu ilanin owner i olan user in advert ids attribute una bu ilani ekler
        if user_response["Status"] != "Success": # islem basarisiz
            result_dict["Status"] = "Fail"
            result_dict["Message"] = f"This advert cannot add to user:{ownerid}. You must delete advert:{advert_id} to provide consistency"
            return result_dict

    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    result_dict["Status"] = "Success"
    result_dict["Message"] = f"New advert successfully created with advert id:{advert_id}"
    result_dict["AdvertID"] = advert_id
    return result_dict


def delete_advert(advertid):
    # PARAMETER TYPES
    # advertid -> int
    
    try:

        advertid = int(advertid)
        TABLE_NAME = 'FakeAdvert'
        result_dict = {} 
        advert_query = retrieve_advert(advertid)
        if advert_query["Status"] == "Fail": # bir sikinti var
            result_dict["Status"] = advert_query["Status"]
            result_dict["Message"] = advert_query["Message"]
            result_dict["AdvertID"] = advertid
            return result_dict

        advert = advert_query["Item"]
        ownerid = advert["OwnerID"] # owner inin AdvertIDs attribute undan bu ilani cikaracagiz

        user_update_query = update_user_list_attributes(ownerid,"AdvertIDs",advertid,"remove")

        if user_update_query["Status"] == "Fail": # bir sikinti var
            result_dict["Status"] = user_update_query["Status"]
            result_dict["Message"] = user_update_query["Message"]
            result_dict["AdvertID"] = advertid
            return result_dict


        delete_statement = f"DELETE FROM {TABLE_NAME} WHERE AdvertID ={advertid}"
        response = client.execute_statement(Statement=delete_statement) 
        #response["Items"]  normalde birsey donmemesi lazim

    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    
    result_dict["Status"] = "Success"
    result_dict["Message"] = f"Advert with advert id:{advertid} is successfully deleted"
    result_dict["AdvertID"] = advertid
    return result_dict


def delete_user(userid):

    try:

        userid = int(userid)
        TABLE_NAME = 'FakeUser'
        result_dict = {} 
        user_query = retrieve_user(userid)
        if user_query["Status"] == "Fail": # bir sikinti var
            result_dict["Status"] = user_query["Status"]
            result_dict["Message"] = user_query["Message"]
            result_dict["UserID"] = userid
            return result_dict

        user = user_query["Item"]
        advert_ids = user["AdvertIDs"]

        # butun advertlari getir
        # gerekeni sil 
        # gerekeni guncelle

        advert_query = retrieve_all_adverts()
        if advert_query["Status"] == "Fail": # bir sikinti var
            result_dict["Status"] = advert_query["Status"]
            result_dict["Message"] = advert_query["Message"]
            result_dict["UserID"] = userid
            return result_dict

        adverts = advert_query["Items"]

        for advert in adverts:
            advert_id = advert["AdvertID"]
            attendees = advert["AttendeeIDs"]
            if advert_id in advert_ids: # eger bu user in bir adverti ise direk silinecek
                response = delete_advert(advert_id)
                if response["Status"] == "Fail": # bir sikinti var
                    result_dict["Status"] = response["Status"]
                    result_dict["Message"] = response["Message"]
                    result_dict["UserID"] = userid
                    return result_dict

            elif userid in attendees: # eger user bu ilanda katilimci ise ilani guncelle yani katilimcilardan bu useri cikar
                response = update_advert_list_attributes(advert_id,"AttendeeIDs",userid,"remove")
                if response["Status"] == "Fail": # bir sikinti var
                    result_dict["Status"] = response["Status"]
                    result_dict["Message"] = response["Message"]
                    result_dict["UserID"] = userid
                    return result_dict

        
        delete_statement = f"DELETE FROM {TABLE_NAME} WHERE UserID ={userid}"
        response = client.execute_statement(Statement=delete_statement) 
        #response["Items"]  normalde birsey donmemesi lazim
        
    except:
        result_dict["Status"] = "Fail"
        result_dict["Message"] = "An exception occured"
        return result_dict

    
    result_dict["Status"] = "Success"
    result_dict["Message"] = f"User with user id:{userid} is successfully deleted"
    result_dict["UserID"] = userid
    return result_dict


def delete_all_tables():
    
    try:

        adverts_query = retrieve_all_adverts()
        result_dict = {}
        if adverts_query["Status"] == "Fail": # fail etti
            result_dict["Status"] = adverts_query["Status"]
            result_dict["Message"] = adverts_query["Message"]
            return result_dict

        adverts = adverts_query["Items"]

        for advert in adverts: # butun advertlar icin

            advertid = advert["AdvertID"]
            advert_delete_query = delete_advert(advertid)
            if advert_delete_query["Status"] == "Fail": # fail etti
                result_dict["Status"] = advert_delete_query["Status"]
                result_dict["Message"] = advert_delete_query["Message"]
                return result_dict

        # donguden ciktiginda butun advertlari silmis demektir

        users_query = retrieve_all_users()
        result_dict = {}
        if users_query["Status"] == "Fail": # fail etti
            result_dict["Status"] = users_query["Status"]
            result_dict["Message"] = users_query["Message"]
            return result_dict

        users = users_query["Items"]

        for user in users: # butun userlar icin

            userid = user["UserID"]
            user_delete_query = delete_user(userid)
            if user_delete_query["Status"] == "Fail": # fail etti
                result_dict["Status"] = user_delete_query["Status"]
                result_dict["Message"] = user_delete_query["Message"]
                return result_dict

        initialize_user_id() # eger butun advertlar ve userlar silindi ise idler initialize edilebilir ve tekrardan user ve advertlara id vermeye 1 den baslanabilir
        initialize_advert_id() 

        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All tables successfully deleted"
        return result_dict
        

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


# ONEMLİ !!!!!   delete_all_users tarzinda bir fonksiyon yok cunku butun userlar silindigi zaman advertlar anlamsiz olur
#                dolayisiyla userlar silindigi zaman advertlarida silmek gerekir.

def delete_all_adverts():

    try:

        adverts_query = retrieve_all_adverts()
        result_dict = {}
        if adverts_query["Status"] == "Fail": # fail etti
            result_dict["Status"] = adverts_query["Status"]
            result_dict["Message"] = adverts_query["Message"]
            return result_dict

        adverts = adverts_query["Items"]

        for advert in adverts: # butun advertlar icin

            advertid = advert["AdvertID"]
            advert_delete_query = delete_advert(advertid)
            if advert_delete_query["Status"] == "Fail": # fail etti
                result_dict["Status"] = advert_delete_query["Status"]
                result_dict["Message"] = advert_delete_query["Message"]
                return result_dict

        # donguden ciktiginda butun advertlari silmis demektir

        users_query = retrieve_all_users()
        if users_query["Status"] == "Fail": # fail etti
            result_dict["Status"] = users_query["Status"]
            result_dict["Message"] = users_query["Message"]
            return result_dict

        users = users_query["Items"]

        for user in users:

            userid = user["UserID"]
            user_update_query = update_user(userid,"AdvertIDs",[]) # userin AdvertIDs attribute u bos liste yapilir
            if user_update_query["Status"] == "Fail": # fail etti
                result_dict["Status"] = user_update_query["Status"]
                result_dict["Message"] = user_update_query["Message"]
                return result_dict

            user_update_query = update_user(userid, "AttendedAdverts",[]) # userin AttendedAdverts attribute unu da bos liste yapacak
            if user_update_query["Status"] == "Fail": # fail etti
                result_dict["Status"] = user_update_query["Status"]
                result_dict["Message"] = user_update_query["Message"]
                return result_dict


        initialize_advert_id() # eger butun advertlar silindi ise advert id initialize edilebilir ve tekrardan advertlara id vermeye 1 den baslanabilir
            
        result_dict["Status"] = "Success"
        result_dict["Message"] = f"All adverts successfully deleted"
        return result_dict
        

    except:
        return {"Status":"Fail", "Message": "An exception occured"}


# Asagida sadece tabloya DUMMY deger eklemeye yarayan fonksiyonlar vardir. 
# Bunlar normalde kullanilmayacaktir.
# ilerleyen asamalarda silineceklerdir

def insert_user_values():

    values = []

    user1 = "'UserID': 1, 'CognitoAuthTokens': ['access token of bkaslan','refresh token of bkaslan'], 'Name': 'Berk', 'Surname':'Karaaslan', 'Username':'bkaslan', 'AdvertIDs':[1,3,7,8], 'Sex':'male', 'Email':'bkaslan@gmail.com', 'Age':22, 'Location':'Ankara-TUR', 'Bio':'This is a bio of bkaslan', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,400], 'WatchedFilms':[100,200,500,400], 'RegistrationDate':'2022-02-19 15:48:36.431698', 'LastLogIn':'2022-02-21 15:48:55.471318',  'LogInCount':10, 'Interests':['Action', 'Thriller'], 'About':'This is an about section of bkaslan' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "                                                                        
    user2 = "'UserID': 2, 'CognitoAuthTokens': ['access token of sceran','refresh token of sceran'], 'Name': 'Suleyman', 'Surname':'Ceran', 'Username':'sceran', 'AdvertIDs':[], 'Sex':'male', 'Email':'sceran@gmail.com', 'Age':21, 'Location':'Ankara-TUR', 'Bio':'This is a bio of sceran', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,400,500], 'WatchedFilms':[300,500,600,100,400], 'RegistrationDate':'2022-01-01 12:35:45.000000', 'LastLogIn':'2022-05-15 23:59:58.171633',  'LogInCount':50, 'Interests':['Drama', 'Horror'], 'About':'This is an about section of sceran' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "                                                                        
    user3 = "'UserID': 3, 'CognitoAuthTokens': ['access token of opolat','refresh token of opolat'], 'Name': 'Omer Faruk', 'Surname':'Polat', 'Username':'opolat', 'AdvertIDs':[6], 'Sex':'male', 'Email':'opolat@gmail.com', 'Age':22, 'Location':'Istanbul-TUR', 'Bio':'This is a bio of opolat', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[400,500,600], 'WatchedFilms':[100,200,300,400,500,600], 'RegistrationDate':'2022-11-27 01:00:17.000000', 'LastLogIn':'2022-11-30 14:20:03.171633',  'LogInCount':18, 'Interests':['Drama', 'Horror', 'Comedy'], 'About':'This is an about section of opolat' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user4 = "'UserID': 4, 'CognitoAuthTokens': ['access token of omujde','refresh token of omujde'], 'Name': 'Ozan', 'Surname':'Mujde', 'Username':'omujde', 'AdvertIDs':[], 'Sex':'male', 'Email':'omujde@gmail.com', 'Age':21, 'Location':'Izmir-TUR', 'Bio':'This is a bio of omujde', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100], 'WatchedFilms':[100,200,500], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':150, 'Interests':['Dark Humor', 'Horror'], 'About':'This is an about section of omujde' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user5 = "'UserID': 5, 'CognitoAuthTokens': ['access token of byalcin','refresh token of byalcin'], 'Name': 'Bugra', 'Surname':'Yalcin', 'Username':'byalcin', 'AdvertIDs':[], 'Sex':'male', 'Email':'byalcin@gmail.com', 'Age':20, 'Location':'Ankara-TUR', 'Bio':'This is a bio of byalcin', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[200], 'WatchedFilms':[100,180,200], 'RegistrationDate':'2022-07-06 03:47:59.161723', 'LastLogIn':'2022-07-06 03:47:59.161723',  'LogInCount':1, 'Interests':['Action', 'Comics'], 'About':'This is an about section of byalcin' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user6 = "'UserID': 6, 'CognitoAuthTokens': ['access token of cbloom','refresh token of cbloom'], 'Name': 'Casey', 'Surname':'Bloom', 'Username':'cbloom', 'AdvertIDs':[], 'Sex':'other', 'Email':'cbloom@gmail.com', 'Age':23, 'Location':'Berlin-GER', 'Bio':'This is a bio of cbloom', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[180,500], 'WatchedFilms':[180,100,300,500,400], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':61, 'Interests':['Horror', 'Anime'], 'About':'This is an about section of cbloom' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user7 = "'UserID': 7, 'CognitoAuthTokens': ['access token of mcartney','refresh token of mcartney'], 'Name': 'Monica', 'Surname':'Cartney', 'Username':'mcartney', 'AdvertIDs':[2,5], 'Sex':'female', 'Email':'mcartney@gmail.com', 'Age':20, 'Location':'Berlin-GER', 'Bio':'This is a bio of mcartney', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[150,100,500], 'WatchedFilms':[150,100,500], 'RegistrationDate':'2021-06-06 09:22:35.101220', 'LastLogIn':'2022-08-13 20:12:44.131638',  'LogInCount':12, 'Interests':['Drama', 'Biography'], 'About':'This is an about section of mcartney' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user8 = "'UserID': 8, 'CognitoAuthTokens': ['access token of dson','refresh token of dson'], 'Name': 'David', 'Surname':'Son', 'Username':'dson', 'AdvertIDs':[], 'Sex':'other', 'Email':'dson@gmail.com', 'Age':28, 'Location':'London-ENG', 'Bio':'This is a bio of dson', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[180,200], 'WatchedFilms':[180,200], 'RegistrationDate':'2021-10-10 17:41:35.001200', 'LastLogIn':'2022-01-31 23:44:12.131739',  'LogInCount':31, 'Interests':['Cartoon'], 'About':'This is an about section of dson' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user9 = "'UserID': 9, 'CognitoAuthTokens': ['access token of edoe','refresh token of edoe'], 'Name': 'Emma', 'Surname':'Doe', 'Username':'edoe', 'AdvertIDs':[], 'Sex':'female', 'Email':'edoe@gmail.com', 'Age':19, 'Location':'London-ENG', 'Bio':'This is a bio of edoe', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[200,400], 'WatchedFilms':[200,100,300,500,400], 'RegistrationDate':'2019-06-08 12:31:33.343536', 'LastLogIn':'2021-11-30 18:03:21.180321',  'LogInCount':72, 'Interests':['Dc', 'Marvel'], 'About':'This is an about section of edoe' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "
    user10 = "'UserID': 10, 'CognitoAuthTokens': ['access token of jdoe','refresh token of jdoe'], 'Name': 'James', 'Surname':'Doe', 'Username':'jdoe', 'AdvertIDs':[4], 'Sex':'male', 'Email':'jdoe@gmail.com', 'Age':24, 'Location':'London-ENG', 'Bio':'This is a bio of jdoe', 'ProfilePhoto': 'This is a normal string profile photo', 'LikedFilms':[100,150,200,400], 'WatchedFilms':[180,150,100,300,500,400], 'RegistrationDate':'2019-06-08 12:31:33.343536', 'LastLogIn':'2021-11-30 18:03:21.180321',  'LogInCount':60, 'Interests':['Civil War', 'Cold War'], 'About':'This is an about section of jdoe' ,'AttendedAdverts': [100,200,300], 'LastUpdateDate': '2019-06-08 12:31:33.343536' "

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


    for i in range(10):
        temp_statement = "INSERT INTO FakeUser VALUE {" + values[i] + "}"
        response = client.execute_statement(Statement=temp_statement) 

    
def insert_advert_values():

    values = []                                                                    
    advert1 = "'AdvertID': 1, 'OwnerID': 1, 'Date': '2022-02-20 20:30:00.000000', 'RegistrationDate':'2022-02-14 19:47:16.001234', 'LastUpdateDate':'2022-02-14 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,3,4,5], 'Status': 'Active', 'FilmID': 100, 'Description': 'this is description', 'PendingRequests': [] "                                                                        
    advert2 = "'AdvertID': 2, 'OwnerID': 7, 'Date': '2022-02-20 20:30:00.000000', 'RegistrationDate':'2022-02-16 19:47:16.001234', 'LastUpdateDate':'2022-02-16 19:47:16.001234', 'Quota': 2, 'AttendeePreference':'male', 'AttendeeIDs': [7,10], 'Status': 'Active', 'FilmID': 150, 'Description': 'this is description', 'PendingRequests': [] "
    advert3 = "'AdvertID': 3, 'OwnerID': 1, 'Date': '2022-02-25 21:00:00.000000', 'RegistrationDate':'2022-02-12 20:33:16.001234', 'LastUpdateDate':'2022-02-12 20:47:16.172144', 'Quota': 3, 'AttendeePreference':'female', 'AttendeeIDs': [1,7,9], 'Status': 'Active', 'FilmID': 200, 'Description': 'this is description', 'PendingRequests': [] "
    advert4 = "'AdvertID': 4, 'OwnerID': 10, 'Date': '2022-02-28 12:30:00.000000', 'RegistrationDate':'2022-02-15 10:09:16.001234', 'LastUpdateDate':'2022-02-15 11:37:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [10,5,6,7,8], 'Status': 'Active', 'FilmID': 180, 'Description': 'this is description', 'PendingRequests': [] "
    advert5 = "'AdvertID': 5, 'OwnerID': 7, 'Date': '2022-02-25 11:00:00.000000', 'RegistrationDate':'2022-02-14 19:47:16.001234', 'LastUpdateDate':'2022-02-15 20:55:18.123456', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [7,2,9,16], 'Status': 'Active', 'FilmID': 100, 'Description': 'this is description', 'PendingRequests': [] "
    advert6 = "'AdvertID': 6, 'OwnerID': 3, 'Date': '2021-05-25 23:00:00.000000', 'RegistrationDate':'2021-05-10 19:47:16.001234', 'LastUpdateDate':'2021-05-10 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [3,2,9,10,6], 'Status': 'Previous', 'FilmID': 300, 'Description': 'this is description', 'PendingRequests': [] "
    advert7 = "'AdvertID': 7, 'OwnerID': 1, 'Date': '2021-01-13 15:30:00.000000', 'RegistrationDate':'2022-01-06 19:47:16.001234', 'LastUpdateDate':'2022-01-06 19:47:16.001234', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,9,10,6], 'Status': 'Previous', 'FilmID': 500, 'Description': 'this is description', 'PendingRequests': [] "
    advert8 = "'AdvertID': 8, 'OwnerID': 1, 'Date': '2021-02-14 20:00:00.000000', 'RegistrationDate':'2021-02-03 12:33:21.124346', 'LastUpdateDate':'2021-02-03 12:33:21.124346', 'Quota': 5, 'AttendeePreference':'all', 'AttendeeIDs': [1,2,9,10,6], 'Status': 'Previous', 'FilmID': 400, 'Description': 'this is description', 'PendingRequests': [] "
    values.append(advert1)
    values.append(advert2)
    values.append(advert3)
    values.append(advert4)
    values.append(advert5)
    values.append(advert6)
    values.append(advert7)
    values.append(advert8)
    
    for i in range(8):
        temp_statement = "INSERT INTO FakeAdvert VALUE {" + values[i] + "}"
        response = client.execute_statement(Statement=temp_statement) 