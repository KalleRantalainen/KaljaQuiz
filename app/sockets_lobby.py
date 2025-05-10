from flask_socketio import emit, join_room, leave_room

from .extensions import socketio
from .player_store import players
from .QuizGame.game_state_store import gameStateStore
from . import rooms


# Kun pelaaja paina Ready! lukee join_game eventin
@socketio.on("join_waiting_room")
def handle_join(data):
    player_id = data["player_id"]
    join_room(rooms.WAITING_ROOM)
    print(f" !!!--@--!!! {player_id} joined WAITING_ROOM", flush=True)


# Kun host valitsee pelin
@socketio.on("game_selected")
def handle_game_selected(data):
    game = data.get("game")

    # Choose the room name for the selected game
    if game == "quizgame":
        target_room = rooms.QUIZGAME_ROOM
    elif game == "coinflipperZ":
        target_room = rooms.COINFLIP_ROOM
    else:
        print(f"Unknown game selected: {game}")
        return

    print()
    print()
    print(f"@@@@@Game selected: {game}. Moving players from waiting_room to {target_room}\n")

    # Emit to clients in waiting_room to switch rooms
    socketio.emit("switch_to_game_room", {"room": target_room}, room="waiting_room")


@socketio.on("join_game_room")
def handle_join_game(data):
    room = data["room"]
    player_id = data["player_id"]
    leave_room(rooms.WAITING_ROOM)
    join_room(room)
    print()
    print()
    print(f" !!!--@--!!! {player_id} joined game room: {room}", flush=True)