import socketio
import threading
import time
import sys

from ai import AgarioAI

if len(sys.argv) != 2:
    print('Usage: python client.py <username>')
    sys.exit(0)

sio = socketio.Client()

agarioAI = AgarioAI()

@sio.event
def connect():
    print('Connected')

@sio.on('welcome')
def on_welcome(playerSettings):
    print('Welcomed. Try to log in as SuperAI')
    playerInfo = playerSettings
    playerInfo.update({
        'name': sys.argv[1],
        'screenWidth': 1920,
        'screenHeight': 1024
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
