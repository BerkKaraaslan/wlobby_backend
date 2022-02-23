import boto3

with open('access_keys.txt') as f:
    lines = f.readlines()

AWS_ACCESS_KEY_ID = lines[0].rstrip()
AWS_SECRET_ACCESS_KEY = lines[1].rstrip()
DEFAULT_REGION = "us-east-1" # AWS wants a region. In my case it is "us-east-1"

client = boto3.client('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = DEFAULT_REGION)

#response = client.get_item( # Now this table contains just dummy data
#    TableName='Student',
#    Key={
#        "StudentID":{
#            "N": "1"
#        }
#    })

def create_user(params): # We will write functions like this function
    pass





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