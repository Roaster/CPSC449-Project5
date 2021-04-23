import boto3
from bottle import route, run, post, get, request
from bottle import response as rs
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from pprint import pprint
from boto3.dynamodb.conditions import Key, Attr
import json


#sendDirectMessage(to, from, message, quickReplies=None)
#Sends a DM to a user. The API call may or may not include a list of quickReplies.
@post('/message/<fromUsername>/<toUsername>/')
def testmethod(fromUsername, toUsername):
    
    data = request.json
    quickReplies = data['quickReplies']

    messageId = str(uuid.uuid4())
    myDate = datetime.now()
    myDate = str(myDate)

    message = createMessage(messageId, fromUsername, data['message'], toUsername, myDate, quickReplies, dynamodb=None)

    rs.status = 201

    return rs

#replyToDirectMessage(messageId, message)
#Replies to a DM. The message may either be text or a quick-reply number. If the message parameter is a quick-reply number, 
#it must have been in response to a  messageId that included a quick-replies field.
@post ('/message/<messageId>')
def replyTo(messageId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    data = request.json
       
    #first get message details
    response = table.get_item(Key={'messageId': messageId})
    if len(response['Item']['quickReply']) > 0:
        try:
            message = response['Item']['quickReply'][int(data['message']) -1]
            print(message)
        except:
            message = data['message']
    else: 
        message = data['message']

    try: 
        quickReplies = data['quickReplies']
    except: 
        quickReplies = []

    replyMessage(messageId, message, quickReplies)

    
    rs.status = 201 

    return rs
    
#listDirectMessagesFor(username)
#Lists the DMs that a user has received.
@get ('/message/<toUser>')
def getDirectMessages(toUser):

    messages = getMessages(toUser)
    if messages is False:
        rs.status = 500
        return rs

    rs.body = json.dumps(messages)
    rs.set_header("Content-Type", "application/json")
   
    return rs



#listRepliesTo(messageId)
@get ('/message/id/<messageId>')
def getRepliesTo(messageId):

    replies = getMessagesId(messageId)
    if replies == []:
        rs.body = "There are no replies."
    else:
        rs.body = json.dumps(replies)
        rs.set_header("Content-Type", "application/json")
    
    return rs
    







    

###############################################################################
#                           Dynamodb methods

def createMessage(messageId, fromUser, text, toUser, timestamp, quickReplies, dynamodb=None):
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
            'quickReply': quickReplies
        }
    )

    response = table2.put_item(
        Item={
            'toUser': toUser,
            'messageId': messageId
        }
    )

    
    return response


def replyMessage(messagedId, message, quickReplies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    #first get message details

    response = table.get_item(Key={'messageId': messagedId})

    fromUser = response['Item']['toUser']

    toUser = response['Item']['fromUser']
    myReplies = response['Item']['replyId']

    messageId = str(uuid.uuid4())
    myDate = datetime.now()
    myDate = str(myDate)
    
    #added the replyId to the others
    myReplies.append(messageId)

    createMessage(messageId, fromUser, message, toUser, myDate, quickReplies)

    update_message(response['Item']['messageId'], myReplies)
    

#Update an entry to add more replyIds
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

    
##########################################################
#Get replies for a messageId
#Does not get used?
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

##########################################################

#Method for creating a table
def create_tables(dynamodb=None):
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
      
    try:
        print(response['Item']['replyId'])
        myResponse = []
        for id in response['Item']['replyId']:
            x = (table.get_item(Key={'messageId': id}))
            myResponse.append(x['Item'])
    except:
        return []


    return myResponse
   
  
   


#gets all the messages from the given user. Uses PK fromUser. Prints them to console
# listDirectMessagesFor(username)
def getMessages(toUser, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('toUsers')
    table2 = dynamodb.Table('DirectMessages')

    response = table.query(
        KeyConditionExpression=Key('toUser').eq(toUser)
    )
    messages = []
    for item in response['Items']:

        text = table2.query(KeyConditionExpression=Key('messageId').eq(item['messageId']))
        #print(text['Items'])
        messages.append(text['Items'])

    return messages

    


#Method for deleting tables
def delete_table(dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')
    table2 = dynamodb.Table('toUsers')
    table.delete()
    table2.delete()

    return 
    

#gets all the messages from the given user. Uses PK fromUser. Prints them to console
# listDirectMessagesFor(username)
def getMessages(toUser, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('toUsers')
    table2 = dynamodb.Table('DirectMessages')
    try:
        response = table.query(
            KeyConditionExpression=Key('toUser').eq(toUser)
        )
    except:
        return False
    messages = []
    for item in response['Items']:

        text = table2.query(KeyConditionExpression=Key('messageId').eq(item['messageId']))

        messages.append(text['Items'])

    return messages

  
###############################################################################
#                           Main method

if __name__ == '__main__':


    run(host='localhost', port=8080, debug=True)

