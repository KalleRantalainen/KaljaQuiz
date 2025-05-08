from flask import jsonify, render_template, Blueprint, request, current_app
import random

from . import coinflipperZ_bp


@coinflipperZ_bp.route("/coin")
def coin_page():
    return render_template("coinflipperZ.html")

@coinflipperZ_bp.route("/api/flip")
def flip_coin():
    user_choice = request.args.get("choice")
    result = random.choice(["Heads", "Tails"])
    win = (user_choice == result)
    return jsonify({"result": result, "win": win})

@coinflipperZ_bp.route("/waiting")
def waiting_screen_host():
    return render_template("host_waiting_room.html")