#!/usr/bin/env python3
#foreman start -f Procfile -e settings.env -p 8080

from bottle import route, run, post, get, error, request, response
import sqlite3
import json

conn = sqlite3.connect('users.db')

c = conn.cursor()

def doesUserExist(user):
    c.execute('SELECT exists(SELECT * FROM users WHERE username=?)', (user,))
    return True if c.fetchone()[0] == 1 else False 


@get('/users/')
def getUsers():
 test = c.execute("select * from users")
 users = []
 for user in test:
     users.append(user[0])

 usersStr = []
 for x in users:
    usersStr.append(x)

 response.set_header = 'Content-Type: json/application'
 response.body = "True. " + usersStr
 response.status = 200

 return response

#curl -d '{"username":"CMan98", "password":"helloworld", "email":"charlie@csu.fullerton.edu"}' -H "Content-Type: application/json" -X POST 'localhost:8080/user/create/'
#curl -d '{"username":"Roaster", "password":"password", "email":"email"}' -H "Content-Type: application/json" -X POST 'localhost:8080/user/create/'
@post('/user/create/')
def createUser():
    data = request.json

    username = str(data['username'])
    password = str(data['password'])
    email = str(data['email'])
    
    if(not doesUserExist(username)):
        newUser = [(username, password, email)]
        c.execute('Insert into users values (?,?,?)', (username, email, password))
        conn.commit()
        response.body = "True"
        response.status = 201
        return response
    else:
        response.body = "The username is already taken."
        response.status = 403
        return response


#  curl -X POST "localhost:8080/Brandon/verify/" -d '{"password":"password"}' -H "Content-Type: application/JSON" -i
@post('/<user>/verify/')
def verifyUser(user):
    data = request.json
    suppliedPassword = data['password']

    c.execute('SELECT exists(SELECT password FROM users WHERE username=?)', (user,))
    accountExist = c.fetchone()[0]

    if(not accountExist):
        response.body = 'The specified account does not exist'
        response.status = 404
        return response
    
    c.execute('SELECT password FROM users WHERE username=?', (user,))
    actualPassword = c.fetchone()[0]
    
    if (suppliedPassword == actualPassword):
        response.body = 'True'
    else:
        response.body = 'False'
    
    response.status = 200
    return response
   
 #  curl -X POST "localhost:8080/Brad/follow/" -d '{"username":"Brandon"}' -H "Content-Type: application/JSON" -i
@post('/<username>/follow/')
def addFollower(username):
    data = request.json

    user1 = data['username'] #user to follow

    c.execute('SELECT exists(SELECT password FROM users WHERE username=?)', (username,))
    verifyUser1 = c.fetchone()[0]

    c.execute('SELECT exists(SELECT password FROM users WHERE username=?)', (user1,))
    verifyUser2 = c.fetchone()[0]

    if (verifyUser1 & verifyUser2):
        c.execute('INSERT into follows (id, user1, user2) values (?,?,?)', ("Null", user1, username))
    
    conn.commit() 

    response.body = "True"
    response.status = 201
    return response


# Sample curl command:
# curl -X POST "localhost:8080/Brad/unfollow/" -d '{"username":"Brandon"}' -H "Content-Type: application/JSON" -i
#user is the user to unfollow
#user1 is following user
@post('/<user>/unfollow/')
def unfollow(user):
    data =request.json
    user1 = data['username']

    if(doesUserExist(user1) and doesUserExist(user)):
        c.execute('SELECT exists(SELECT * FROM follows WHERE user1=? AND user2=?)', (user1,user))
        if(c.fetchone()[0]): #if 1 / true there exists a row where user1 follows user
            c.execute('DELETE FROM follows WHERE user1=? AND user2=?', (user1, user))
            conn.commit()
            response.status = 204
            return response
        else:
            response.body = "There is no followings with these users"
            response.status = 200
            return response
    else:
        response.body = "These accounts do not exists"
        response.status = 200
        return response

#curl -X GET "localhost:8080/Brandon/followers/" -i"
@get('/<user>/followers/')
def getFollowers(user):
    c.execute('SELECT user2 FROM follows WHERE user1=?', (user,))
    response.body = json.dumps(c.fetchall())
    response.status = 200
    return response


#run(host='localhost', port=8080, debug=True)


