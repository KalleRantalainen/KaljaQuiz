from flask import Blueprint

quizgame_bp = Blueprint(
    "quizgame",
    __name__,
    url_prefix="/quizgame",
    template_folder="templates",
    static_folder="static",
)

from . import routes
from . import sockets
from . import game_state_store