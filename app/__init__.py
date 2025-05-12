# Init flask app
from flask import Flask
from flask_session import Session

from .QuizGame import quizgame_bp
from .coinflipperZ import coinflipperZ_bp

from .extensions import socketio


def create_app(host_ip, port):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "secret_key"

    app.config['SESSION_TYPE'] = 'filesystem'
    # Tallennetaan osoite, jonka kautta käyttäjät pääsee liittymään.
    app.config['HOST_IP'] = host_ip
    app.config['PORT'] = port

    Session(app)

    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(quizgame_bp)
    app.register_blueprint(coinflipperZ_bp)
    
    origins = [
        f"http://{host_ip}:{port}",
        "http://localhost:8080"
    ]
    print()
    print("ORIGINS:")
    print(origins)
    print()

    socketio.init_app(app, cors_allowed_origins=origins)
    #socketio.init_app(app, async_mode='eventlet')

    # Tämä tekee HOST_IP ja PORT muttujista accessible jokaisella
    # templatella.
    @app.context_processor
    def inject_config():
        return {
            'HOST_IP': host_ip,
            'PORT': port
        }

    return app