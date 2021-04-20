#command to start dynamodb
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

#command to view all items in the DirectMessages table
aws dynamodb scan --table-name DirectMessages --endpoint-url http://localhost:8000

#command to view all tables
aws dynamodb list-tables --endpoint-url http://localhost:8000


#command to send a new DirectMessage
curl -H "Content-Type: application/json" -d '{"message":"Hello World"}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/


#command to reply to a directmessage
curl -H "Content-Type: application/json" -d '{"message":"I am replying from the endpoint!"}' -X POST http://localhost:8080/message/<messageId>


#command to get messages to <username>
curl -X GET http://localhost:8080/message/<username>


#command to get replies to messageId
curl -X GET http://localhost:8080/message/id/<messageId>


requirements
dynamodb
java
curl