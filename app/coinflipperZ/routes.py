from flask import jsonify, render_template, Blueprint, request, current_app
import random

from . import coinflipperZ_bp


@coinflipperZ_bp.route("/coin")
def coin_page():
    is_host = request.args.get("host") == "1"
    return render_template("coinflipperZ.html", is_host=is_host)


@coinflipperZ_bp.route("/waiting")
def waiting_screen_host():
    return render_template("host_waiting_room.html")