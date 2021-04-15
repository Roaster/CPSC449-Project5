#command to start dynamodb
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

#command to view all items in the DirectMessages table
aws dynamodb scan --table-name DirectMessages --endpoint-url http://localhost:8000

#command to view all tables
aws dynamodb list-tables --endpoint-url http://localhost:8000

