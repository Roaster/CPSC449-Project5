1. To start all services(users, timelines and directmessages) navigate to the correct directory then execute:
    foreman start -e settings.env -f Procfile -p 8080

2. The services are now available for requests.

    sendDirectMessage(to, from, message, quickReplies=None)

    curl -H "Content-Type: application/json" -d '{"message":"Hello World", "quickReplies":[]}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/


    replyToDirectMessage(messageId, message)

    curl -H "Content-Type: application/json" -d '{"message":"I am replying from the endpoint!"}' -X POST http://localhost:8080/message/<messageId>


    listDirectMessagesFor(username)

    curl -X GET http://localhost:8080/message/<username>


    listRepliesTo(messageId)

    curl -X GET http://localhost:8080/message/id/<messageId>




#command to start dynamodb
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

#command to view all items in the DirectMessages table
aws dynamodb scan --table-name DirectMessages --endpoint-url http://localhost:8000

#command to view all tables
aws dynamodb list-tables --endpoint-url http://localhost:8000


#command to send a new DirectMessage
curl -H "Content-Type: application/json" -d '{"message":"Hello World"}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/
curl -H "Content-Type: application/json" -d '{"message":"Hello World", "quickReplies":["Hello!", "Goodbye!"]}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/

#command to reply to a directmessage
curl -H "Content-Type: application/json" -d '{"message":"I am replying from the endpoint!"}' -X POST http://localhost:8080/message/<messageId>


#command to get messages to <username>
curl -X GET http://localhost:8080/message/<username>


#command to get replies to messageId
curl -X GET http://localhost:8080/message/id/<messageId>


requirements
dynamodbjava -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
java
curl
