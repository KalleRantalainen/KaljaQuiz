from flask import Blueprint

coniflipper_bp = Blueprint(
    "coinflip",
    __name__,
    url_prefix="/coinflip",
    template_folder="templates",
    static_folder="static",
)

from . import routes
from . import sockets_coin
