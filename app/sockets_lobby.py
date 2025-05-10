from flask_socketio import emit, join_room, leave_room
from flask import request
from .extensions import socketio
from .player_store import players
from .QuizGame.game_state_store import gameStateStore, CURRENT_GAME_ROOM
from . import rooms


# Kun pelaaja paina Ready! lukee join_game eventin
@socketio.on("join_waiting_room")
def handle_join(data):
    player_id = data["player_id"]
    print(f"@@@@@@@@@@@@@@@{CURRENT_GAME_ROOM}@@@@@@@@@@@@@")

        # JOs host jo valinnut pelin, lähetetään myöhässä liittyneet nykyiseen huoneeseen
    if CURRENT_GAME_ROOM == "quizgame_room":
        print(f"!!!!!!!!!!!!!!!!!Sending {player_id} directly to game room: {CURRENT_GAME_ROOM}")
        socketio.emit("switch_to_game_room", {"room": CURRENT_GAME_ROOM}, room=rooms.WAITING_ROOM)

    else:
        join_room(rooms.WAITING_ROOM)
        print(f" !!!--@--!!! {player_id} joined WAITING_ROOM", flush=True)

    

# Kun host valitsee pelin
@socketio.on("game_selected")
def handle_game_selected(data):
    global CURRENT_GAME_ROOM

    game = data.get("game")

    # Choose the room name for the selected game
    if game == "quizgame":
        CURRENT_GAME_ROOM = rooms.QUIZGAME_ROOM
    elif game == "coinflipperZ":
        CURRENT_GAME_ROOM = rooms.COINFLIP_ROOM
    else:
        print(f"Unknown game selected: {game}")
        return

    print()
    print()
    print(f"@@@@@Game selected: {game}. Moving players from waiting_room to {CURRENT_GAME_ROOM}\n")

    # Emit to clients in waiting_room to switch rooms
    socketio.emit("switch_to_game_room", {"room": CURRENT_GAME_ROOM}, room=rooms.WAITING_ROOM)


@socketio.on("join_game_room")
def handle_join_game(data):
    room = data["room"]
    player_id = data["player_id"]
    leave_room(rooms.WAITING_ROOM)
    join_room(room)
    print()
    print()
    print(f" !!!--@--!!! {player_id} joined game room: {room}", flush=True)