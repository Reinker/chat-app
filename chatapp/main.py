from chatapp import app
from chatapp import db
from flask import Flask, render_template, request, redirect, url_for, jsonify, templating
from flask_session import Session
from flask_httpauth import HTTPBasicAuth
from flask_socketio import SocketIO, emit, disconnect
from markupsafe import escape
import json

async_mode = None
socket = SocketIO(app, async_mode=async_mode)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    res = db.db.select_user(username, password)
    if res.count() == 1:
        for v in res:
            return v

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def home():
    current_user = str(auth.current_user()['_id'])
    if request.method == 'POST':
        res = request.data.decode()
        res_json = json.loads(res)
        roomname = res_json['roomname']
        member = res_json['member']
        db.db.insert_chatroom(roomname, member)

    res = db.db.select_chatrooms(current_user)
    rooms = []
    for v in res :
        rooms.append(v)
    return render_template('index.html', rooms=rooms)

@app.route('/room/<room_id>')
@auth.login_required
def room(room_id):
    res = db.db.select_chatroom(room_id)
    current_user = auth.current_user()
    return render_template('chatroom.html', async_mode=socket.async_mode, room=res, user_id=str(current_user['_id']), username=str(current_user['name']))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', error='')
    else:
        res = request.data.decode()
        res_json = json.loads(res)
        username = res_json['username']
        password = res_json['password']
        res = db.db.insert_user(username, password)
        if res is None:
            return redirect(url_for('signup'))

        return redirect(url_for('home')) 

@app.route('/getuser')
@auth.login_required
def get_user_info():
    current_user = auth.current_user()
    return jsonify(username=str(current_user['name']), user_id=str(current_user['_id'])), 200

@app.route('/getusers')
@auth.login_required
def get_users_info():
    res = db.db.select_all_user()
    users = []
    for v in res :
        users.append({'name': str(v['name']), 'user_id': str(v['_id'])})

    return jsonify(users), 200

@app.route('/getroom/<room_id>')
@auth.login_required
def get_room_info(room_id):
    res = db.db.select_chatroom(room_id)
    return jsonify(room_id=str(res['_id']), roomname=str(res['name']), chats=res['chats']), 200

@socket.on('send')
def send_message(message):
    db.db.add_chat(message['room_id'], message['username'], message['user_id'], message['chat'])
    emit('receive', message)

if __name__ == '__main__':
    print ('main')
    socket.run(app)

