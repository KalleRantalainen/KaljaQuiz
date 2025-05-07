from flask import render_template, redirect, url_for, abort, current_app
import io
import base64
import qrcode

from . import quizgame_bp

def generate_qr(url):
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_b64

# Host waiting screen
@quizgame_bp.route("/waiting")
def waiting_screen_host():
    host_ip = current_app.config.get("HOST_IP", "127.0.0.1")
    port = current_app.config.get("PORT", 8080)
    url = f"http://{host_ip}:{port}/user"

    qr_code = generate_qr(url)

    return render_template("host_waiting.html", qr_code=qr_code)
