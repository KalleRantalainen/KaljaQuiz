from flask_socketio import emit, join_room
from app.extensions import socketio
from app.player_store import players
from QuizGame.game_state_store import gameStateStore
import random
from flask import request

# Store choices by user_id or socket id
choices = {}
COINFLIP_ROOM = "coinflipperZ_room"

@socketio.on("start_coinflip")
def handle_start_game():
    print("!!! start_coinflip received from host, broadcasting to users", flush=True)
    emit("start_coinflip", broadcast=True, to="players")


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