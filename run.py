# Docker file ajaa tämän tiedoston ensimmäisenä -> Käynnistää pelin

import os
import socket
import eventlet
eventlet.monkey_patch()

from app import create_app
from app.extensions import socketio
from app import sockets_lobby

# Haetaan koneen ip osoite, koska dockerin portti suoraan ei toimi
def get_host_ip():
    env_ip = os.environ.get("HOST_IP")
    if env_ip:
        return env_ip

    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        return "127.0.0.1"

PORT = int(os.environ.get("PORT", 8080))
HOST_IP = get_host_ip()

app = create_app(HOST_IP, PORT)

if __name__ == "__main__":
    print("HOST IP IN run.py:", HOST_IP)
    print(f"User URL: http://{HOST_IP}:{PORT}/user")
    print(f"User URL: http://{HOST_IP}:{PORT}/host")

    socketio.run(app, host="0.0.0.0", port=PORT, debug=True)