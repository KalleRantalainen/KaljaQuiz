# Init flask app
from flask import Flask
from flask_session import Session

from .QuizGame import quizgame_bp
from .coinflipperZ import coinflipperZ_bp

from .extensions import socketio, db
from .database import models


def create_app(host_ip, port):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "secret_key"

    app.config['SESSION_TYPE'] = 'filesystem'
    # Tallennetaan osoite, jonka kautta käyttäjät pääsee liittymään.
    app.config['HOST_IP'] = host_ip
    app.config['PORT'] = port

    # Tietokannan configurointi
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Luodaan puuttuvat taulut tietokantaan. Tätä ei kai
    # kannata kutsua aina, sitten kun ohjelma on valmis vaan 
    # pelkästään ensimmäisen runin yhteydessä
    with app.app_context():
        db.create_all()

    Session(app)

    from app.routes import main

    app.register_blueprint(main)
    app.register_blueprint(quizgame_bp)
    app.register_blueprint(coinflipperZ_bp)
    
    origins = [
        f"http://{host_ip}:{port}",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
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