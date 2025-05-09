from flask_socketio import emit, join_room
from app.extensions import socketio
from app.player_store import players

QUIZGAME_ROOM = "quizgame_room"

# Tämä socket ottaa lukee join_game eventin.
# event tulee kun pelaaja antaa nimensä ja painaa nappia.
@socketio.on("join_game")
def handle_join(data):
    player_id = data["player_id"]
    join_room(QUIZGAME_ROOM)
    print(f" !!! {player_id} joined game", flush=True)

@socketio.on('start_quizgame')
def handle_start_quizgame(data):
    print("Host started quiz game (server)")
    # Emittoidaan pelaajille täältä sama eventti (huoneeseen players, koska pelaajat ovat siellä)
    emit('start_quizgame', room=QUIZGAME_ROOM)