from flask import render_template, redirect, url_for, abort, current_app, session
import io
import base64
import qrcode
from threading import Lock

from . import quizgame_bp
from app.player_store import players
from .game_state_store import gameStateStore

ready_lock = Lock() # Lukko gameStateStoren päivittämistä varten

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

    print("URL:", url, flush=True)
    
    qr_code = generate_qr(url)

    host_id = "host_id_should_be_here"
    if 'host_id' in session:
        host_id = session['host_id']

    return render_template("host_waiting.html", qr_code=qr_code, host_id=host_id)


# Pelaajien näkymä pelissä, route ei muutu pelin aikana, näkymä päivittyy dynaamisesti.
@quizgame_bp.route("/player_game")
def player_game():
    print("PLAYERS IN PLAYER_STORE:", players, flush=True)
    print("  PREVIOUS PLAYER COUNT:", gameStateStore.get_player_count(), flush=True)
    # Käytetään lukkoa ettei tule concurrency ongelmia.
    # Useampi pelaaja ohjataan tänne kerralla eikä moni
    # saa muokata samaa muuttujaa yhtäaikaa.
    with ready_lock:
        gameStateStore.increase_player_count()
    print("  UPDATED PLAYER COUNT:", gameStateStore.get_player_count(), flush=True)
    return render_template("quizgame_player.html", user_id=session['user_id'])

# Route hostin partial viewien lataamista varten
@quizgame_bp.route("/host_partial/<view_name>")
def get_host_partial(view_name):
    host_ip = current_app.config.get("HOST_IP", "127.0.0.1")
    port = current_app.config.get("PORT", 8080)
    url = f"http://{host_ip}:{port}/user"
    
    qr_code = generate_qr(url)

    if view_name == "waiting":
        return render_template("/partials/host_waiting_view.html", qr_code=qr_code)
    elif view_name == "game":
        return render_template("/partials/host_game_view.html")
    else:
        return "Not Found", 404