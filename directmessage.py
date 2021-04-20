import boto3
from bottle import route, run, post, get, request
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from pprint import pprint
from boto3.dynamodb.conditions import Key, Attr
import json


#def sendMessage()
@post('/message/<fromUsername>/<toUsername>/')
def testmethod(fromUsername, toUsername):
    
    data = request.json
    print(data['message'])
    messageId = str(uuid.uuid4())
    #messageId = '1'
    myDate = datetime.now()
    myDate = str(myDate)
    message = createMessage(messageId, fromUsername, data['message'], toUsername, myDate, dynamodb=None)



#@get('/message/replies/<messageId>')
#def getReplies(messageId):


###############################################################################
#                           Dynamodb methods

def createMessage(messageId, fromUser, text, toUser, timestamp, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    table2 = dynamodb.Table('toUsers')

    response = table.put_item(
        Item={
            'messageId': messageId,
            'fromUser': fromUser,
            'text': text,
            'toUser': toUser,
            'timestamp': timestamp,
            'replyId' : [],
            'quickReply': []
        }
    )

    response = table2.put_item(
        Item={
            'toUser': toUser,
            'messageId': messageId
        }
    )

    return response


def replyMessage(messagedId, message, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    #first get message details

    response = table.get_item(Key={'messageId': messagedId})

    toUser = response['Item']['toUser']

    fromUser = response['Item']['fromUser']
    myReplies = response['Item']['replyId']

    messageId = str(uuid.uuid4())
    myDate = datetime.now()
    myDate = str(myDate)
    
    #added the replyId to the others
    myReplies.append(messageId)

    createMessage(messageId, fromUser, message, toUser, myDate)
    update_message(response['Item']['messageId'], myReplies)
    

#Needed to update changed entries
def update_message(messageId, replyId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')

    response = table.update_item(
        Key={
            'messageId': messageId
        },
        UpdateExpression="set replyId=:r",
        ExpressionAttributeValues={
            ':r': replyId
            
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

    


def getReplies(messagedId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    
    table = dynamodb.Table('DirectMessages')

    response = table.query(
        KeyConditionExpression=Key('messagedId').eq(messagedId)
    )

    for item in response['Items']:
        print(item)
    #items = response['Items']
    #print(items)



#Method for creating a table
def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='DirectMessages',
        KeySchema=[
            {
                'AttributeName': 'messageId',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'messageId',
                'AttributeType': 'S'
            }
            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table = dynamodb.create_table(
        TableName='toUsers',
        KeySchema=[
            {
                'AttributeName': 'toUser',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'messageId',
                'KeyType': 'RANGE'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'toUser',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'messageId',
                'AttributeType': 'S'
            }
            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    
    return table


# listRepliesTo(messageId)
def getMessagesId(messageId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    response = table.get_item(Key={'messageId': messageId})

    print(response['Item']['replyId'])
    myResponse = []
    for id in response['Item']['replyId']:
        x = (table.get_item(Key={'messageId': id}))
        myResponse.append(x['Item']['text'])

    for message in myResponse:
        print(message)
   
  
   


#gets all the messages from the given user. Uses PK fromUser. Prints them to console
#
def getMessages(fromUser, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')

    response = table.query(
        KeyConditionExpression=Key('fromUser').eq(fromUser)
    )
    items = response['Items']
    print(items)

#Method for deleting tables
def delete_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    #select a table to delete
    table = dynamodb.Table('DirectMessages')
    table2 = dynamodb.Table('toUsers')
    table.delete()
    table2.delete()



###############################################################################
#                           Main method

if __name__ == '__main__':
    #create table
    #delete_table()
    #movie_table = create_movie_table()
    
    #replyMessage("bb15e213-57b2-4178-a4c5-b610f4313335","I am replying to you!")
    #replyMessage("bb15e213-57b2-4178-a4c5-b610f4313335","Please work!")
    getMessagesId("bb15e213-57b2-4178-a4c5-b610f4313335")

    run(host='localhost', port=8080, debug=True)
    #message = testmethod('andy', 'test')
    #delete table
    
    #to test this, create messages using testmethod above. It will print all messages created by given fromUser
    #getMessages('andy')
    #if getMessages:
     #   print("Get message succeeded:")
      #  pprint(getMessages, sort_dicts=False)
    #
    
    #print("Table status:", movie_table.table_status)