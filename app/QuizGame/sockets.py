from flask_socketio import emit, join_room
from app.extensions import socketio
from app.player_store import players
#from QuizGameLogic.GameStateStore import game_state_store

answered_players = set()

@socketio.on("join_game")
def handle_join(data):
    player_id = data["player_id"]
    join_room("players")
    print(f"{player_id} joined game", flush=True)

@socketio.on("start_game_loop")
def handle_start_game(data):
    print("Starting game loop", flush=True)
    # Emit first question
    emit("next_question", {
        "question": "What is the capital of France?",
        "time_limit": 20
    }, room="players")

@socketio.on("answer_submitted")
def handle_answer(data):
    player_id = data["player_id"]
    answer = data["answer"]
    print(f"{player_id} answered: {answer}", flush=True)
    answered_players.add(player_id)

    # Check if all players have answered
    if len(answered_players) == len(players):
        emit("question_done", {}, room="players")
        answered_players.clear()