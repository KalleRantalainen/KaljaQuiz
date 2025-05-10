from flask_socketio import emit, join_room

from .extensions import socketio
from .player_store import players
from QuizGame.game_state_store import gameStateStore

WAITING_ROOM = "waiting_room"

# Kun pelaaja paina Ready! lukee join_game eventin
@socketio.on("join_waiting_room")
def handle_join(data):
    player_id = data["player_id"]
    join_room(WAITING_ROOM)
    print(f" !!!--@--!!! {player_id} joined WAITING_ROOM", flush=True)

@socketio.on("switch_to_game_room")
def handle_join_game(data):
    game = data['room']
    
    if game == "quizgame":
        socketio.emit("join_quizgame")
    elif game == "coinflipperZ":
        socketio.emit("join_coingame")

@socketio.on("game_selected")
def handle_game_selected(data):
    game = data.get("game")

    # Choose the room name for the selected game
    if game == "quizgame":
        target_room = "quizgame"
    elif game == "coinflipperZ":
        target_room = "coinflipperZ"
    else:
        print(f"Unknown game selected: {game}")
        return

    print()
    print(f"Game selected: {game}. Moving players from waiting_room to {target_room}\n")

    # Emit to clients in waiting_room to switch rooms
    socketio.emit("switch_to_game_room", {"room": target_room}, room="waiting_room")
