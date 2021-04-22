import boto3
from datetime import datetime
from directmessage import replyMessage

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
    
    return 'Tables created'


def delete_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    #select a table to delete
    table = dynamodb.Table('DirectMessages')
    table2 = dynamodb.Table('toUsers')
    table.delete()
    table2.delete()


def filltables(dynamodb=None):
    myDate = datetime.now()
    myDate = str(myDate)
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    #add data to table
    table = dynamodb.Table('DirectMessages')
    table2 = dynamodb.Table('toUsers')
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '1',
                'fromUser': 'johndoe',
                'text': 'This is a test message!',
                'toUser': 'andy',
                'timestamp': myDate,
                'replyId' : [],
                'quickReply': ["Hello!","No!","Yes!"]
            }
        )
    with table2.batch_writer() as batch2:
        batch2.put_item(
            Item={
                'toUser': 'andy',
                'messageId': '1'
            }

        )

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '2',
                'fromUser': 'johndoe',
                'text': 'This is a second test message!',
                'toUser': 'andy',
                'timestamp': myDate,
                'replyId' : [],
                'quickReply': []
            }
        )
    with table2.batch_writer() as batch2:
        batch2.put_item(
            Item={
                'toUser': 'andy',
                'messageId': '2'
            }

        )

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '3',
                'fromUser': 'brandon',
                'text': 'Hello there!',
                'toUser': 'johndoe',
                'timestamp': myDate,
                'replyId' : [],
                'quickReply': ['On my way!']
            }
        )
    with table2.batch_writer() as batch2:
        batch2.put_item(
            Item={
                'toUser': 'johndoe',
                'messageId': '3'
            }

        )

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '4',
                'fromUser': 'johndoe',
                'text': 'Where is the car?',
                'toUser': 'andy',
                'timestamp': myDate,
                'replyId' : [],
                'quickReply': []
            }
        )
    with table2.batch_writer() as batch2:
        batch2.put_item(
            Item={
                'toUser': 'andy',
                'messageId': '4'
            }

        )

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '5',
                'fromUser': 'andy',
                'text': 'This is a second test message!',
                'toUser': 'brandon',
                'timestamp': myDate,
                'replyId' : [],
                'quickReply': ['Why?',"No!"]
            }
        )
    with table2.batch_writer() as batch2:
        batch2.put_item(
            Item={
                'toUser': 'brandon',
                'messageId': '5'
            }

        )
    replyMessage('2', '', '0')
    replyMessage('3', 'General Kenobi!', '')



if __name__ == '__main__':
#create tables then fill those tables, uncomment to delete
    create_tables()
    filltables()
#delete_table()