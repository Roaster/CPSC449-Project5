import boto3
from bottle import route, run, post, get
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from pprint import pprint
from boto3.dynamodb.conditions import Key, Attr

#endpoint for sending a message from one user to another
#def sendMessage()
@post('/message/<fromUsername>/<toUsername>/')
def testmethod(fromUsername, toUsername):
    print(fromUsername + "\t" + toUsername)
    messageId = str(uuid.uuid4())
    #messageId = '1'
    myDate = datetime.now()
    myDate = str(myDate)
    message = createMessage(messageId, fromUsername, "This is a test", toUsername, myDate, dynamodb=None)


###############################################################################
#                           Dynamodb methods

def createMessage(messageId, fromUser, text, toUser, timestamp, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')

    response = table.put_item(
        Item={
            'messageId': messageId,
            'fromUser': fromUser,
            'text': text,
            'toUser': toUser,
            'timestamp': timestamp
        }
    )

    return response


#Method for creating a table
def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='DirectMessages',
        KeySchema=[
            {
                'AttributeName': 'fromUser',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'messageId',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'messageId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'fromUser',
                'AttributeType': 'S'
            },
                        {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

#gets all the messages from the given user. Uses PK fromUser. Prints them to console
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
    table.delete()



###############################################################################
#                           Main method

if __name__ == '__main__':
    #create table
    #movie_table = create_movie_table()
    #message = testmethod('andy', 'test')
    #delete table
    #delete_table()
    #to test this, create messages using testmethod above. It will print all messages created by given fromUser
    #getMessages('andy')
    #if getMessages:
     #   print("Get message succeeded:")
      #  pprint(getMessages, sort_dicts=False)
    run(host='localhost', port=8080, debug=True)
    print("Table status:", movie_table.table_status)
