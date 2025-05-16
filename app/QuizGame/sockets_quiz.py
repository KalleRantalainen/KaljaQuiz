from flask_socketio import emit, join_room
from time import sleep
import eventlet

from app.extensions import socketio
from app.player_store import players
from .game_state_store import gameStateStore
from ..rooms import LOBBY

"""Join_game on nyt join_lobby ja käytetään kaikkiin peleihin"""

# Quizgamen aloitus, muille peleille voi tehdä samanlaisen joskus
@socketio.on('start_quizgame')
def handle_start_quizgame(data):
    print("Host started quiz game (server)")
    # Emittoidaan pelaajille täältä sama eventti (huoneeseen players, koska pelaajat ovat siellä)
    emit('start_quizgame', room=LOBBY)

# Alustaa pelin aloittamalla
@socketio.on('player_ready')
def handle_player_ready(data):
    print()
    print("In player_ready:", flush=True)
    expected_count = len(players)
    print(" - Expected count:", expected_count, flush=True)
    current_count = gameStateStore.get_player_count()
    print(" - Current count:", current_count, flush=True)
    if current_count == expected_count:
        print(" - Expected count = current count, emit start")
        emit('start_game', room=LOBBY)

        sleep(8)
        emit('next_question', room=LOBBY)



# Next question pitää fixaa. Jos tekee tällä tavalla
# niin clientit saa kiinni mut host ei. Jos emittaa
# hostin js koodista niin host saa kiinni mutta clientit ei.
# Nyt menen nukkumaan.
@socketio.on('next_question')
def handle_next_question(data):
    print("HANDLING NEXT QUESTION")
    emit("next_question", room=LOBBY)
