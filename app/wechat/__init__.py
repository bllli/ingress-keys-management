from flask import Blueprint

keybot = Blueprint('keybot', __name__)

from . import views