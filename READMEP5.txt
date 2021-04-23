1. Initialize databases with users.sql and timelines.sql
    cat users.sql | sqlite3 users.db
    cat timelines.sql | sqlite3 timelines.db

2. To start all services(users, timelines and directmessages) navigate to the correct directory then execute:
    foreman start -e settings.env -f Procfile -p 8080

3. The services are now available for requests.

    #DIRECTMESSAGES

    sendDirectMessage(to, from, message, quickReplies=None)

    curl -H "Content-Type: application/json" -d '{"message":"Hello World", "quickReplies":[]}' -X POST http://localhost:8080/message/<fromUser>/<toUser>/


    replyToDirectMessage(messageId, message)

    curl -H "Content-Type: application/json" -d '{"message":"I am replying from the endpoint!"}' -X POST http://localhost:8080/message/<messageId>


    listDirectMessagesFor(username)

    curl -X GET http://localhost:8080/message/<username>


    listRepliesTo(messageId)

    curl -X GET http://localhost:8080/message/id/<messageId>



    #USERS AND TIMELINES FROM PROJECT 2

    #BE SURE TO CHECK THE PORTS AFTER RUNNING FOREMAN. THE USERS SERVICE SHOULD BE ON PORT 8180
    # AND THE TIMELINES ON PORT 8280

    createUser(username, email, password)
    curl -d '{"username":"Andy", "password":"password", "email":"email"}' -H "Content-Type: application/json" -X POST 'localhost:8180/user/create/'

    authenticateUser(username, password)
    curl  -d '{"password":"password1"}'-H "Content-Type: application/JSON" -X POST "localhost:8180/Brandon/verify/" -i 

    addFollower(username, usernameToFollow)
    curl  -d '{"username":"Brandon"}' -H "Content-Type: application/JSON" -X POST "localhost:8180/Brandon/follow/" -i

    removeFollower(username, usernameToRemove)
    curl  -d '{"username":"Brandon"}' -H "Content-Type: application/JSON" -X POST "localhost:8180/Brandon/unfollow/" -i

    getUserTimeline(username)
    curl -X GET "localhost:8081/timeline/Brandon/" -i

    postTweet(username, text)
    curl  -d '{"username":"Brandon", "text":"My first post!"}' -H "Content-Type: application/JSON" -X POST "localhost:8280/post/new/" -i

    getHomeTimeline(username)
    curl -X POST "localhost:8280/timeline/Brandon/home/" -d '{"follower":["Brandon", "Brad"]}' -H "Content-Type: application/JSON"  - 

    getPublicTimeline()
    curl -X GET "localhost:8280/timeline/" -i  