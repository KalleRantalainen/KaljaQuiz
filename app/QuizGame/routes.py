from flask import render_template, redirect, url_for, abort, current_app, jsonify, session
import io
import base64
import qrcode
from flask_socketio import emit

from app.player_store import players # Get the dict where the players are stored
from app.game_state_store import game_state_store
#from app import socketio

from . import quizgame_bp

def generate_qr(url):
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_b64

# Host waiting screen
@quizgame_bp.route("/waiting")
def waiting_screen_host():
    host_ip = current_app.config.get("HOST_IP", "127.0.0.1")
    port = current_app.config.get("PORT", 8080)
    url = f"http://{host_ip}:{port}/user"

    qr_code = generate_qr(url)

    return render_template("host_waiting.html", qr_code=qr_code, host_id=session['host_id'])


# Triggered when start-game button is pressed
@quizgame_bp.route("/game")
def host_game_view():
    print("Host in the /game route", flush=True)
    if 'host_id' not in session:
        return redirect(url_for("main.host"))  # block non-hosts
    return render_template("host_game.html")


@quizgame_bp.route("/play", methods=["GET"])
def player_game_view():
    print("User in the /play route", flush=True)
    if 'user_id' not in session:
        return redirect(url_for("main.user"))  # block non-players
    return render_template("player_game.html", user_id=session['user_id'])

