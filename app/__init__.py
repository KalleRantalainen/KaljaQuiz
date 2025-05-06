# Init flask app
from flask import Flask
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"

    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)

    from app.routes import main

    app.register_blueprint(main)

    return app