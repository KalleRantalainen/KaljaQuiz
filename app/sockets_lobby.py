from flask_socketio import emit, join_room, leave_room
from flask import request, session
from .extensions import socketio
from .player_store import players, sid_to_user
from .QuizGame.game_state_store import gameStateStore
from .rooms import LOBBY

# Tämä socket ottaa lukee join_game eventin.
# event tulee kun pelaaja antaa nimensä ja painaa nappia.
@socketio.on("join_lobby")
def handle_join(data):
    user_id = session.get("user_id")
    sid_to_user[request.sid] = user_id
    print(f"@@@@@@@@@@@@@@@{LOBBY}@@@@@@@@@@@@@")

    join_room(LOBBY)
    print(f" !!!--@--!!! {user_id} joined game", flush=True)




