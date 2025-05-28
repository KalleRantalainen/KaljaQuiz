from flask import render_template, redirect, url_for, abort, current_app, session, jsonify
import io
import base64
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from threading import Lock
from types import SimpleNamespace
from flask import request
import re


from . import quizgame_bp
from app.player_store import players
from .game_state_store import gameStateStore
from .QuizGameLogic import getQuestions #ota poijes
from .quizgame_running import questionRajapinta


ready_lock = Lock() # Lukko gameStateStoren päivittämistä varten

# Muuntaa rgba, rgb tai hex värit int tupleiks
def format_color(color):
    if color.startswith("rgba") or color.startswith("rgb"):
        match = re.findall(r'\d+', color)
        if len(match) >= 3:
            try:
                r, g, b = int(match[0]), int(match[1]), int(match[2])
                color = (r, g, b)  # ← tuple instead of hex
            except ValueError:
                color = (0, 0, 0)
    elif re.match(r'^#[0-9a-fA-F]{6}$', color):
        try:
            color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # ← hex → RGB tuple
        except ValueError:
            color = (0, 0, 0)
    else:
        color = (0, 0, 0)
    return color

# Luo qr koodin halutuilla väreillä
def generate_qr(url, colorBg="#000000", colorHl="#ffffff"):
    colorBg = format_color(colorBg)
    colorHl = format_color(colorHl)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make()

    img = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(back_color=colorBg, front_color=colorHl)
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_b64

# JS postaa requestin tänne kun waiting näkymä on latautunut.
# Tämä palauttaa qr koodin oikeilla väreillä
@quizgame_bp.route("/generate_qr", methods=["POST"])
def generate_colored_qr():
    data = request.get_json()

    host_ip = current_app.config.get("HOST_IP", "127.0.0.1")
    port = current_app.config.get("PORT", 8080)
    url = f"http://{host_ip}:{port}/user"

    colorHighlight = data.get("colorHl", "#000000")
    colorBg = data.get("colorBg", "#ffffff")

    qr_code = generate_qr(url, colorBg, colorHighlight)

    return jsonify({"qr": qr_code})

# Host waiting screen
@quizgame_bp.route("/waiting")
def waiting_screen_host():
    host_ip = current_app.config.get("HOST_IP", "127.0.0.1")
    port = current_app.config.get("PORT", 8080)
    url = f"http://{host_ip}:{port}/user"

    print("URL:", url, flush=True)
    
    #qr_code = generate_qr(url)

    host_id = "host_id_should_be_here"
    if 'host_id' in session:
        host_id = session['host_id']

    return render_template("host_waiting.html", host_id=host_id) #qr_code=qr_code


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
    
    #qr_code = generate_qr(url)

    if view_name == "waiting":
        return render_template("/partials/host_partials/host_waiting_view.html") #, qr_code=qr_code
    elif view_name == "host_question":
        return render_template("/partials/host_partials/host_question_view.html")
    else:
        return "Not Found", 404
    
    

@quizgame_bp.route('/show_answers_partial')
def show_answers_partial():
    answer = request.args.get('answer', '')
    player_count = len(players)
    return render_template('partials/host_partials/show_answers.html', answer=answer, player_count=player_count)


#Tähän uudesta questionAPIsta
@quizgame_bp.route("/quest_partial")
def get_example_question():
    #---------------
    random_quest = questionRajapinta.get_rand_question()
    #answer = questionRajapinta.get_answer_by_question(random_quest)
    player_count = len(players)
    return render_template("partials/host_partials/question.html", question=random_quest, player_count=player_count)


@quizgame_bp.route("/player_partial/<view_name>")
def get_player_partial(view_name):

    if view_name == "submit":
        return render_template("/partials/player_partials/player_submit.html")
    elif view_name == "answerSubmitted":
        # Kun vastaus lähetetty --> oottelu näkymä
        return render_template("/partials/player_partials/submit_waiting.html")
    elif view_name == "afterVotingScreen":
        return render_template("partials/player_partials/after_vote_screen.html")
    else:
        return "Not Found", 404
    

@quizgame_bp.route("/voting_phase_partial")
def get_player_voting_phase():
    user_id = session.get("user_id")
    return render_template("partials/player_partials/voting_phase.html", user_id=user_id)


@quizgame_bp.route("/round_result_partial")
def get_player_points():
    return render_template("partials/host_partials/round_results.html", player_data=players)

@quizgame_bp.route("/final_results_partial")
def load_final_result():
    return render_template("partials/host_partials/final_results.html")

@quizgame_bp.route("/player_ending_partial/")
def player_ending_partial():
    return render_template("partials/player_partials/player_ending.html")