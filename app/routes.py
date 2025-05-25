from flask import Blueprint, session, render_template, request, redirect, url_for, jsonify
import uuid

from app.player_store import players

main = Blueprint("main", __name__)

@main.route('/')
def frontpage():
    return render_template('frontpage.html')

# Main route for the host. Tää pitäs ehkä suojata jotenkin, ettei useempi pääse liittymään?
@main.route('/host')
def host():
    if 'host_id' not in session:
        session['host_id'] = str(uuid.uuid4())
        print("HOST ID GENERATED:", session['host_id'], flush=True)
    print("TEST", flush=True)
    return render_template('host.html')

@main.route("/host/waiting")
def host_waiting_room():
    game = request.args.get("game")
    
    if game == "coinflipperZ":
        return redirect("/coinflipperZ/waiting")
    elif game == "quizgame":
        # Pistin tänne redirecting, että tää host käy quizgame/waiting routen kautta
        # koska siellä lasketaan ainakin qr koodi. Jossain kohtaa ehkä jotain muutakin.
        return redirect("/quizgame/waiting")
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
        players[session["user_id"]] = {
            "name": name,
            "quizgame": {
                "answer": None,
                "points": 0,
                "voted": False
            },
            "coingame":{
                # Jos tarvii muille peleille
            }
        }
    return redirect(url_for("main.user_waiting"))


# Route to the user waiting screen
@main.route('/user-waiting', methods=["GET"])
def user_waiting():
    return render_template("user_waiting.html", user_id=session['user_id'])


# JSON endpoint to get the player names
@main.route("/players", methods=["GET"])
def list_players():
    return jsonify([data["name"] for data in players.values()])

