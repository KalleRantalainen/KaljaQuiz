from flask_socketio import SocketIO
# Alustetaan socketio täällä niin ei tule circular import
# erroreita.
socketio = SocketIO(cors_allowed_origins="*")