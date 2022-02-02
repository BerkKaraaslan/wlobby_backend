import boto3

with open('access_keys.txt') as f:
    lines = f.readlines()

AWS_ACCESS_KEY_ID = lines[0].rstrip()
AWS_SECRET_ACCESS_KEY = lines[1].rstrip()
DEFAULT_REGION = "us-east-1" # AWS wants a region. In my case it is "us-east-1"

client = boto3.client('dynamodb', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = DEFAULT_REGION)

response = client.get_item( # Now this table contains just dummy data
    TableName='Student',
    Key={
        "StudentID":{
            "N": "1"
        }
    })

# This response contains 2 part of information. "Item" and "ResponseMetadata"
# "Item" is the meaningful part for us
# We can use "Item" part like a json object. 

meaningful_item = response["Item"] # It is a dictionary object, we can print all key-value pairs in this dictionary
#Note: This dictionary's values are dictionary too. 

#Surname {'S': 'Doe'}
#Age {'N': '20'}
#StudentID {'N': '1'}
#Name {'S': 'John'}

# Below lines are examples of meaningful_item's key-value pairs
# Keys of this dictionaries are Attribute Type, ex: 'S' means String
# Values of this dictionaries are actual values that comes from DynamoDB

for item in meaningful_item:
    print(item, meaningful_item[item])