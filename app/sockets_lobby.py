from flask_socketio import emit, join_room, leave_room
from flask import request
from .extensions import socketio
from .player_store import players
from .QuizGame.game_state_store import gameStateStore, CURRENT_GAME_ROOM
from . import rooms


# Kun pelaaja paina Ready! lukee join_game eventin
@socketio.on("join_room")
def handle_join(data):
    player_id = data["player_id"]
    print(f"@@@@@@@@@@@@@@@{rooms.LOBBY}@@@@@@@@@@@@@")

    join_room(rooms.LOBBY)
    print(f" !!!--@--!!! {player_id} joined WAITING_ROOM", flush=True)

