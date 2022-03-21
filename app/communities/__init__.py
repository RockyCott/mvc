from flask import Blueprint

comms = Blueprint('communities', __name__, url_prefix='/communities')

from . import views