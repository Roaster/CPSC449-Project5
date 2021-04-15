import boto3

def createMessage(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('DirectMessages')

    response = table.put_item(
        Item={
            'messageId': 1,
            'fromUser': 'Brandon',
            'text': 'Hello world',
            'toUser': 'Admin',
            'timestamp': 'soon'
        }
    )

    return response




def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='DirectMessages',
        KeySchema=[
            {
                'AttributeName': 'messageId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'fromUser',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'messageId',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'fromUser',
                'AttributeType': 'S'
            },
            

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

#Method for deleting tables
def delete_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    #select a table to delete
    table = dynamodb.Table('DirectMessages')
    table.delete()


if __name__ == '__main__':
    #create table
    #movie_table = create_movie_table()
    message = createMessage()
    #delete table
    #delete_table()

    #print("Table status:", movie_table.table_status)