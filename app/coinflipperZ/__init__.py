from flask import Blueprint

coinflipperZ_bp = Blueprint(
    "coinflipperZ",
    __name__,
    url_prefix="/coinflipperZ",
    template_folder="templates",
    static_folder="static",
)

from . import routes