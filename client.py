import socketio
import threading
import time
import sys
import os

import ai_load as ai

if len(sys.argv) < 3:
    print('Usage: python client.py <username> <ainame> <optional args>')
    sys.exit(0)

sio = socketio.Client()

try:
    agarioAI = ai.get_ai(sys.argv[2])(*sys.argv[3:])
except Exception as e:
    print(e)
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
    agarioAI.other_players = []
    for user in userData:
        if 'id' not in user:
            agarioAI.local_player = user
        else:
            agarioAI.other_players.append(user)
    
    agarioAI.foods = foodsList
    
    agarioAI.virus = virusList 


    target = agarioAI.next_target()
    if target:
        sio.emit('0', target)

@sio.on('RIP')
def on_rip():
    print('RIP...')
    sio.close()
    sys.exit(0)

#@sio.on('serverUpdateAllPlayers')


@sio.on('playerJoin')
def on_playerJoin(data):
    print('[INFO] Player ' + str(data['name']) + ' joined')


@sio.event
def disconnect():
    print('Disconnected')

addr = os.getenv('ADDR', '192.168.11.40:3000')
sio.connect('http://' + addr + '?type=player')
sio.emit('respawn')
sio.wait()
