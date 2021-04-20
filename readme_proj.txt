#command to start dynamodb
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

#command to view all items in the DirectMessages table
aws dynamodb scan --table-name DirectMessages --endpoint-url http://localhost:8000

#command to view all tables
aws dynamodb list-tables --endpoint-url http://localhost:8000


#command to send a new DirectMessages
curl -H "Content-Type: application/json" -d '{"message":"Hello World"}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/


requirements
dynamodb
java
curl