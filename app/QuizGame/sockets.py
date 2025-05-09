from flask_socketio import emit, join_room
from app.extensions import socketio
from app.player_store import players

# Tämä socket ottaa lukee join_game eventin.
# event tulee kun pelaaja antaa nimensä ja painaa nappia.
@socketio.on("join_game")
def handle_join(data):
    player_id = data["player_id"]
    join_room("players")
    print(f" !!!--@--!!! {player_id} joined game", flush=True)