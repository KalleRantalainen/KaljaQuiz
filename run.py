# Docker file ajaa tämän tiedoston ensimmäisenä -> Käynnistää pelin

import os
import socket

from app import create_app
from app import socketio

app = create_app()

# Haetaan koneen ip osoite, koska dockerin portti suoraan ei toimi
def get_host_ip():
    env_ip = os.environ.get("HOST_IP")
    if env_ip:
        return env_ip

    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        return "127.0.0.1"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host_ip = get_host_ip()
    print(f"User URL: http://{host_ip}:{port}/user")
    # Tallennetaan osoite, jonka kautta käyttäjät pääsee liittymään.
    app.config['HOST_IP'] = host_ip
    app.config['PORT'] = port
    socketio.run(app, host="0.0.0.0", port=port, debug=True)