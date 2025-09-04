from flask import Blueprint

profile = Blueprint('profile', __name__)

from . import routes  # noqa: E402, F401

