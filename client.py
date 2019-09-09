import socketio
import threading
import time
import sys

import ai

if len(sys.argv) != 3:
    print('Usage: python client.py <username> <ainame>')
    sys.exit(0)

sio = socketio.Client()

try:
    agarioAI = ai.get_ai(sys.argv[2])()
except:
    print('No such AI. Exiting')
    sys.exit(1)

@sio.event
def connect():
    print('Connected')

@sio.on('welcome')
def on_welcome(playerSettings):
    print('Welcomed. Try to log in as SuperAI')
    playerInfo = playerSettings
    playerInfo.update({
        'name': sys.argv[1],
        'screenWidth': 1000,
        'screenHeight': 550
    })
    sio.emit('gotit', playerInfo)

@sio.on('serverTellPlayerMove')
def on_serverTellPlayerMove(userData, foodsList, massList, virusList):
    for user in userData:
        if 'id' not in user:
            agarioAI.local_player = user
        else:
            agarioAI.other_players.clear()
            agarioAI.other_players[user['id']] = user
    
    agarioAI.foods = foodsList
    
    agarioAI.virus = virusList 


    target = agarioAI.next_target()
    if target:
        sio.emit('0', target)

@sio.on('serverUpdateAllPlayers')


@sio.on('playerJoin')
def on_playerJoin(data):
    print('[INFO] Player ' + str(data['name']) + ' joined')


@sio.event
def disconnect():
    print('Disconnected')

sio.connect('http://192.168.11.40:3000?type=player')
sio.emit('respawn')
sio.wait()
