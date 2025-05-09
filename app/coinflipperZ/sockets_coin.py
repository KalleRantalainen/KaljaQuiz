from flask_socketio import emit, join_room
from app.extensions import socketio
from app.player_store import players
import random
from flask import request

# Store choices by user_id or socket id
choices = {}

@socketio.on("start_game")
def handle_start_game():
    print("Received start_game from host") 
    socketio.emit("start_game")  # Send to everyone

@socketio.on("connect")
def handle_connect():
    print("User connected:", request.sid)

@socketio.on("player_choice")
def handle_choice(data):
    choices[request.sid] = data["choice"]

# Emitoi tuloksen ja animaation
@socketio.on("flip_coin")
def handle_flip():
    result = random.choice(["Heads", "Tails"])
    for sid, choice in choices.items():
        win = (choice == result)
        socketio.emit("flip_result", {"result": result, "win": win}, to=sid)
    
    # Also show coin flip to everyone without result
    socketio.emit("animate_flip", {"result": result})

@socketio.on("disconnect")
def handle_disconnect():
    choices.pop(request.sid, None)