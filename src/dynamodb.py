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

response = client.execute_statement(Statement=statement) 

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

print(response["Items"])  

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