from flask import render_template, redirect, url_for, abort
from . import quizgame_bp

# Host waiting screen
@quizgame_bp.route("/waiting")
def waiting_screen_host():
    return render_template("host_waiting.html")
