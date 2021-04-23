#!/usr/bin/env python3

from bottle import route, run, post, get, error, request, response
import sqlite3
import json
import datetime

conn = sqlite3.connect('timelines.db')

c = conn.cursor()




#curl -X GET "localhost:8180/timeline/Brandon/" -i
@get('/timeline/<username>/')
def getUserTimeline(username):

    c.execute('SELECT * FROM posts WHERE username=? ORDER BY id desc LIMIT 25', (username,))

    posts = c.fetchall()
    print(json.dumps(posts))
    response.body = json.dumps(posts)
    response.status = 200
    response.set_header = ('Content-Type: application/JSON')
    return response
    
 
#curl -X POST "localhost:8180/post/new/" -H "Content-Type: application/JSON" -d '{"username":"Brandon", "text":"Error!!"}' -i
@post('/post/new/')
def createPost():
    data = request.json
    print(data)
    username = data['username']
    post = data['text']
    c.execute('INSERT into posts values (NULL,?,?,?)', (str(username), str(post), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    response.body = "Success"
    response.status = 201
    return response


#curl -X GET "localhost:8180/timeline/" -i  
@get('/timeline/')
def getAllTimeline():
    c.execute('Select * from posts ORDER BY id desc LIMIT 25 ')
    response.body = json.dumps(c.fetchall())
    response.status = 200

    return response

#curl -X POST "localhost:8180/timeline/Brandon/home/" -d '{"follower":["Brandon", "Brad"]}' -H "Content-Type: application/JSON"  -i 
@post('/timeline/<username>/home/')
def getHomeTimeline(username):
    data = request.json
    print(data['follower'])
    myTimeline=[]

    for follow in data['follower']:
        c.execute('SELECT * FROM posts WHERE username=? ORDER BY id desc LIMIT 25', (follow,))
        myTimeline.append(c.fetchall())

    response.body = json.dumps(myTimeline)
    response.status = 201

    return response

#run(host='localhost', port=8082, debug=True)