from flask import Blueprint

portal = Blueprint('portal', __name__)

from . import views, errors
