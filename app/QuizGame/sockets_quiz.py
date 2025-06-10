from flask_socketio import emit, join_room
from time import sleep
import eventlet
from flask import session, request
import random

from app.extensions import socketio
from app.player_store import players, sid_to_user
from .game_state_store import gameStateStore
from ..rooms import QUIZ_ROOM
from .quizgame_running import questionRajapinta

"""Join_game on nyt join_quizgame_lobby ja käytetään kaikkiin peleihin"""

# Quizgamen aloitus, muille peleille voi tehdä samanlaisen joskus
@socketio.on('start_quizgame')
def handle_start_quizgame(data):
    print("Host started quiz game (server)")
    # Emittoidaan pelaajille täältä sama eventti
    emit('start_quizgame', room=QUIZ_ROOM)

# Alustaa pelin aloittamalla
@socketio.on('player_ready')
def handle_player_ready(data):
    print()
    print("In player_ready:", flush=True)
    expected_count = len(players)
    print(" - Expected count:", expected_count, flush=True)
    current_count = gameStateStore.get_player_count()
    print(" - Current count:", current_count, flush=True)
    if current_count >= expected_count:
        print(" - Expected count = current count, emit start")
        emit('start_game', room=QUIZ_ROOM)

        sleep(5)
        emit('next_question', room=QUIZ_ROOM)
        emit('next_submit', room=QUIZ_ROOM)


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
    answers_payload.append(
        {
            "user_id": "computer",
            "name": "correct",
            "answer": correct_answer
        }
    )

    random.shuffle(answers_payload)
    
    emit('answers', {
        'correct_answer': correct_answer,
        'answers_list': answers_payload
    }, room=QUIZ_ROOM)

    # Reset for next round
    for p in players.values():
        if "quizgame" in p:
            p["quizgame"]["answer"] = None
            p["quizgame"]["voted"] = False


@socketio.on('next_submit')
def handle_next_submit():
    emit('next_submit', room=QUIZ_ROOM)

@socketio.on('return_player_answer')
def handle_player_answer(data):
    answer = data.get("answer")
    user_id = session.get("user_id")

    if user_id in players:
        players[user_id]["quizgame"]["answer"] = answer
        players[user_id]["quizgame"]["new_points"] = 0
        print(" ======== PELAAJAN UUDET PISTEET NOLLATTU, TILANNE NYT:", players[user_id]["quizgame"]["new_points"], flush=True)
        print(f"Player '{players[user_id]['name']}' answered: {answer}")
        
        emit("update_player_counter", room=QUIZ_ROOM)
    else:
        print("Unknown user tried to submit an answer.")


@socketio.on("voted_a_player")
def handle_vote(data):
    user_id = session.get("user_id")
    voted_player = data.get("voted_player")
    players[user_id]["quizgame"]["voted"] = True

    if voted_player in players:
        players[voted_player]["quizgame"]["points"] += 1
        players[voted_player]["quizgame"]["new_points"] += 1
        print(" ======== PELAAJALLE +1 UUSI PISTE, TILANNE NYT:", players[voted_player]["quizgame"]["new_points"], flush=True)
        print("Pelaaja ", players[voted_player]["name"], " sai äänen pelaajalta ", players[session.get("user_id")])
        print("Pelaajalla on nyt ", players[voted_player]["quizgame"]["points"], " pistettä")
    else:
        print("PELAAJA ÄÄNESTI TUNTEMATONTA")
    
    emit("update_player_counter", room=QUIZ_ROOM)
    check_all_voted()

@socketio.on("voted_real_answer")
def handle_real_vote():
    user_id = session.get("user_id")
    players[user_id]["quizgame"]["voted"] = True

    players[session.get("user_id")]["quizgame"]["points"] += 1
    players[user_id]["quizgame"]["new_points"] += 1
    print(" ======== PELAAJALLE +1 UUSI PISTE, OIKEA VASTAUS, TILANNE NYT:", players[user_id]["quizgame"]["new_points"], flush=True)
    print("Pelaaja valitsi oikean vastauksen")

    emit("update_player_counter", room=QUIZ_ROOM)
    check_all_voted()


def check_all_voted():
    if all(p.get("quizgame", {}).get("voted") for p in players.values()):
        socketio.emit("everyone_voted", room=QUIZ_ROOM)


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
    emit('player_finisher', room=QUIZ_ROOM)
    

#Nyt saadaan sessionin kautta personoidut lopetukset sijoituksen mukaan
@socketio.on("load_player_ending")
def handle_player_end():
    #user_id = session.get("user_id")
    sid = request.sid
    user_id = sid_to_user.get(sid)

    if not user_id:
        emit('final_player_result', {"message": "Session expired. Please rejoin."}, to=sid)
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
        emit('final_player_result', {"message": "You were not found in the results."}, to=sid)
        return

    # Generate message
    if position == 1:
        message = f"🏆 Olet ansainnut illallisen jonka tarjoaa Kalle! Wohooo!"
    elif position == 2:
        message = f"🥈 Olet vähän hidas kaveri"
    elif position == 3:
        message = f"🥉 Olet aika idiootti tyyppi!"
    else:
        message = f"{position} sija, jää vaan kotiin ensi kerralla. 😬"

    emit('final_player_result', {"message": message, "position": position}, to=sid)
    