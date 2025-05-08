from flask import Blueprint, session, render_template, request, redirect, url_for, jsonify
import uuid
from QuizGameLogic.getQuestions import example_get_questions

from app.player_store import players

main = Blueprint("main", __name__)

# Main route for the host. Tää pitäs ehkä suojata jotenkin, ettei useempi pääse liittymään?
@main.route('/host')
def host():
    return render_template('host.html')

@main.route("/host/waiting")
def host_waiting_room():
    game = request.args.get("game")
    
    if game == "coinflipperZ":
        return render_template("host_waiting_room.html")
    elif game == "quizgame":
        return render_template("host_waiting.html")
    else:
        return "Unknown game", 400


# Route for the players to register/give their name
@main.route('/user', methods=["GET"])
def user():
    # Luodaan uusi id käyttäjälle, jos ei jo ole.
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template("registration.html", user_id=session['user_id'])


# Register the user to the store
@main.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    if name:
        players[session["user_id"]] = name
    return redirect(url_for("main.user_waiting"))


# Route to the user waiting screen
@main.route('/user-waiting', methods=["GET"])
def user_waiting():
    return render_template("user_waiting.html")


# JSON endpoint to get the player names
@main.route("/players", methods=["GET"])
def list_players():
    return jsonify(list(players.values()))

