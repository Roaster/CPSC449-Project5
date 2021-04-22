jave: java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
directmessages: python3 directmessage.py
users: python3 -m bottle users -b localhost:$PORT
timelines:  python3 -m bottle timelines -b localhost:$PORT