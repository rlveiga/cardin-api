from flask import Blueprint

card = Blueprint('card', __name__, url_prefix='/cards')

from . import views