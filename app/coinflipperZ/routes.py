from flask import render_template

from . import coniflipper_bp

@coniflipper_bp.route("/waiting")
def waiting_screen_host():
    return render_template("host_view.html")

# Partials
@coniflipper_bp.route("/waiting_players")
def waiting_players():
    return render_template("partials/host_waiting.html")