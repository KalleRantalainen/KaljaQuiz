from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Alustetaan socketio täällä niin ei tule circular import
# erroreita.
socketio = SocketIO(cors_allowed_origins="*")

# Alustetaan tietokanta
db = SQLAlchemy()

# Tässä on varmaan suurin osa muutoksista. Sen sijaan että
# käytettiin cors_allowed_origins=["*"], käytetäänkin localhostia
# ja ip osotetta.
socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:8080",
        # ip address is added here in __init__.py
    ],
    logger=True,
    engineio_logger=True,
    async_handlers=True
)