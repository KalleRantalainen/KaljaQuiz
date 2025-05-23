from flask_socketio import emit, join_room
from time import sleep
import eventlet
from flask import session

from app.extensions import socketio
from app.player_store import players
from .game_state_store import gameStateStore
from ..rooms import LOBBY
from .quizgame_running import questionRajapinta

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

        sleep(5)
        emit('next_question', room=LOBBY)
        emit('next_submit', room=LOBBY)


# Tämässä näytetään vastaukset hostin näytölle
@socketio.on('show_answers')
def handle_show_answers(data):

    question = data.get('question')
    correct_answer = questionRajapinta.get_answer_by_question(question)

    # Collect quizgame answers
    answers_payload = [
        {
            "user_id": user_id,
            "name": p["name"],
            "answer": p.get("quizgame", {}).get("answer", "")
        }
        for user_id, p in players.items()
    ]

    emit('answers', {
        'correct_answer': correct_answer,
        'player_answers': answers_payload
    }, room=LOBBY)

    # Reset for next round
    for p in players.values():
        if "quizgame" in p:
            p["quizgame"]["answer"] = None


@socketio.on('next_submit')
def handle_next_submit():
    emit('next_submit', room=LOBBY)

@socketio.on('return_player_answer')
def handle_player_answer(data):
    answer = data.get("answer")
    user_id = session.get("user_id")

    if user_id in players:
        players[user_id]["quizgame"]["answer"] = answer
        print(f"Player '{players[user_id]['name']}' answered: {answer}")
    else:
        print("Unknown user tried to submit an answer.")

@socketio.on("voted_a_player")
def handle_vote(data):
    voted_player = data.get("voted_player")

    if voted_player in players:
        players[voted_player]["quizgame"]["points"] += 1
        print("###################################")
        print("Pelaaja ", players[voted_player]["name"], " sai äänen pelaajalta ", players[session.get("user_id")])
        print("Pelaajalla on nyt ", players[voted_player]["quizgame"]["points"], " pistettä")
        print("###################################")
    else:
        print("PELAAJA ÄÄNESTI TUNTEMATONTA")

@socketio.on("voted_real_answer")
def handle_real_vote():
    players[session.get("user_id")]["quizgame"]["points"] += 1
    print("Pelaaja valitsi oikean vastauksen")

@socketio.on("end_game")
def handle_end_game():
    sorted_players = sorted(
        players.items(),
        key=lambda item: item[1]["quizgame"]["points"],
        reverse=True  # Highest first
    )

    result_payload = [
        {
            "user_id": user_id,
            "name": player['name'],
            "points": player['quizgame']['points']

        }
        for user_id, player in sorted_players
    ]

    #Host näytölle kaikkien tulokset
    emit('final_results', {"results": result_payload})

    #Pelaajien näytölle oma sijoitus ja onnittelut ehkä
    #emit player_finisher -> socket.emit end_players -> emit personoidut onnittelut
    emit('player_finisher', room=LOBBY)
    

#Nyt saadaan sessionin kautta personoidut lopetukset sijoituksen mukaan
@socketio.on("load_player_ending")
def handle_player_end():
    user_id = session.get("user_id")
    if not user_id:
        emit('final_player_result', {"message": "Session expired. Please rejoin."}, room=LOBBY)
        return

    # Sort players by points (same as before)
    sorted_players = sorted(
        players.items(),
        key=lambda item: item[1]["quizgame"]["points"],
        reverse=True
    )

    # Find the position (1-based index)
    position = None
    for i, (uid, _) in enumerate(sorted_players):
        if uid == user_id:
            position = i + 1
            break

    # Fallback if not found
    if position is None:
        emit('final_player_result', {"message": "You were not found in the results."}, room=LOBBY)
        return

    # Generate message
    if position == 1:
        message = f"🏆 You're the CHAMPION! 1st place — amazing work!"
    elif position == 2:
        message = f"🥈 2nd place — so close to glory!"
    elif position == 3:
        message = f"🥉 3rd place — a worthy podium finish!"
    else:
        message = f"{position}th place... maybe stick to Uno next time. 😬"

    emit('final_player_result', {"message": message, "position": position}, room=LOBBY)
    