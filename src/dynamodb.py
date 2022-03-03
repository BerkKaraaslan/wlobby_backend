import boto3

with open('access_keys.txt') as f:
    lines = f.readlines()

AWS_ACCESS_KEY_ID = lines[0].rstrip()
AWS_SECRET_ACCESS_KEY = lines[1].rstrip()
DEFAULT_REGION = "us-east-1" # AWS wants a region. In my case it is "us-east-1"

client = boto3.client('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = DEFAULT_REGION)




# CRUD Functions

# CREATE Functions

INITIAL_LOGIN_VALUE = 1 # Login count bunu tutacak

def create_user(name,surname,username,sex,email,age,location,bio,profilephoto,likedfilms,interests,about):
    # UserId id_generator.py dosyasından alınacak ve tekrar o dosyadan ıd yi update etmek icin increment user id cagrilacak
    # Name, Surname ve Username parametre olarak alinacak
    # AdvertIDs basta bos bir liste olarak db de tutulacak
    # Sex, Email,Age parametre olarak alinacak
    # Location, Bio, ProfilePhoto parametre olarak alinacak
    # LikedFilms i movie id listesi olarak parametre alacak
    # WatchedFilms basta bos bir liste olarak db de tutulacak
    # RegistrationDate current time.py dosyasından alınacak
    # LastLogIn basta RegistrationDate ile esitlenecek yani ayni degeri tutacak
    # Daha sonra user a update ler geldikce ve giris yapdikca artacak
    # LogInCount da initial deger olarak 1 tutacak
    # Interests parametre olarak alinacak ve bu parametrenin type i string list olacak
    # About da string olarak parametre alinacak

    # User icin de LastUpdateDate TUTULACAK ve User da bir degisikligin son yapildigi zamani tutacak

    # baslangicta bunun degeri registration date olacak

    return 1

def create_advert(ownerid,date,quota,preference,filmid):
    # AdvertID id_generator.py dan alinacak ve tekrar o dosyadan id yi update etmek icin increment advert id cagrilacak
    # Ownerid parametre olarak alinacak
    # Date i parametre olarak alacak. date ilanin ne zaman icin planlandigini gosterir. Date i belirtilen formatta (current time.py formatında) string olarak alacak
    # RegistrationDate ilanin ne zaman olusturuldugunu tutacak bunu current_time.py dan alacak
    # LastUpdateDate basta registrationdate e esit olacak daha sonra ilan icin bir update geldigi zaman bu guncellenecek
    # Quota int parametre olacak alinacak
    # AttendeePreference string parametre olarak belirtilen formatlarda alinacak
    # AttendeeIDs basta sadece owner in id sini iceren bir int listesi olacak
    # Status basta direk active olacak cunku gecmis bir tarihe ilan olusturmaya izin vermeyecegiz o yuzden parametre olmasina gerek yok
    # FilmID bize direk frontend den gelecek int parametre seklinde kaydedilecek

    return 1


# RETRIEVE Functions


def retrieve_user(userid):
    # UserID si verilen user i dondurecek
    # Dondururken formatin iyi olmasina dikkat et 
    # Yani or {Id: {N: 5}} gibi degil {Id: 5} seklinde olmali yani attribute type larini gosteren parametreleri at
    # Id["N"] i gibi yaparak direk 5 degeri alinabilir
    pass


def retrieve_advert(advertid):
    # AdvertID si verilen advert i dondurecek
    # Dondururken formatin iyi olmasina dikkat et 
    # Yani or {Id: {N: 5}} gibi degil {Id: 5} seklinde olmali yani attribute type larini gosteren parametreleri at
    pass

def retrieve_all_adverts(userid):
    # verilen user id ye sahip userin butun ilanlarini dondurur
    pass


# UPDATE Functions

# butun normal attribute lar icin update fonksiyonlari olacak hem user hem de advert icin

# Ayrica user in liked films lerine film ekle veya liked films lerinden film cikar gibi fonksiyonlar da olacak

# Aybi sekilde watched films ve AdvertIDs icine bir seyler ekleme ve cikarma fonksiyonlari da olacak

# Ayrica advert in da attendeıds kismi icin update fonksiyonu olacak

# cikar kisimlari  delete functions bolomunde olacak

# bir update oldugu zaman hem user hem de advert de lastupdatedate current time ile guncellenecek


# DELETE Functions

# Normal attributelar icin delete fonksiyonu yazilmayacak

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

def create_user(params): # We will write functions like this function
    pass


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