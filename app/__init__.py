# Init flask app
from flask import Flask
from flask_session import Session

from .QuizGame import quizgame_bp


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "secret_key"

    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)

    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(quizgame_bp)

    return app