from flask_socketio import emit, join_room, leave_room
from flask import request, session
from .extensions import socketio
from .player_store import players, sid_to_user
from .QuizGame.game_state_store import gameStateStore
from .rooms import CURRENT_ROOM

# Tämä socket ottaa lukee join_game eventin.
# event tulee kun pelaaja antaa nimensä ja painaa nappia.
@socketio.on("join_quizgame_lobby")
def handle_join():
    user_id = session.get("user_id")
    sid_to_user[request.sid] = user_id
    print(CURRENT_ROOM["game"])

    join_room(CURRENT_ROOM["game"])
    print(f" !!!--@--!!! {user_id} joined game", flush=True)


@socketio.on("join_coinflip_lobby")
def handle_join_coinflip():
    join_room(CURRENT_ROOM["game"])
    print(CURRENT_ROOM["game"])

@socketio.on("host_join_lobby")
def handle_host_join_quiz():
    join_room(CURRENT_ROOM["game"])