from pymongo import MongoClient
from bson import ObjectId
import hashlib
import pprint
from datetime import datetime

MONGO_PORT=27017
MONGO_ADDRESS='127.0.0.1'
USERNAME='chatapp'
PASSWORD='chatapp'

def connect_to_db():
    client = MongoClient(MONGO_ADDRESS, MONGO_PORT)
    db = client['chatapp']
    db.authenticate(USERNAME, PASSWORD)
    return db

def select_chatrooms(user_id):
    chatroom = connect_to_db()['chatroom']
    return chatroom.find({'member': {'$in': [user_id]}})

def select_chatroom(room_id):
    chatroom = connect_to_db()['chatroom']
    return chatroom.find_one({'_id': ObjectId(room_id)})

def insert_chatroom(roomname, member):
    if len(member) < 1:
        return 

    chatroom = connect_to_db()['chatroom']
    return chatroom.insert_one({
        'name': roomname,
        'member': member,
        'chats': [],
        'date': datetime.now().isoformat()
    })

def add_chat(room_id, username, user_id, chat):
    chatroom = connect_to_db()['chatroom']
    return chatroom.update({'_id': ObjectId(room_id)}, {
        '$push' : {'chats': {
            'user_id': user_id, 
            'user_name': username, 
            'chat': chat,
            'date': datetime.now().isoformat()
        }}
    })


def add_member(room_id, user_id):
    chatroom = connect_to_db()['chatroom']
    return chatroom.update({'_id': ObjectId(room_id)}, {
        '$push' : {'member': user_id}
    })

def select_user(username, password):
    user = connect_to_db()['user']
    return user.find({
        'name': username, 
        'password': hashlib.sha256(password.encode('utf-8')).hexdigest()
    })

def user_already_exist(username):
    user = connect_to_db()['user']
    res = user.find({'name': username})
    if res.count() > 0:
        return True
        
    return False

def select_all_user():
    user = connect_to_db()['user']
    return user.find({})

def insert_user(username, password):
    if user_already_exist(username):
        print('user already exits')
        return None

    user = connect_to_db()['user']
    return user.insert_one({
        'name': username, 
        'password': hashlib.sha256(password.encode('utf-8')).hexdigest(), 
        'date': datetime.now().isoformat()
    })

