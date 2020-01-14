from flask import Blueprint

collection = Blueprint('collection', __name__, url_prefix='/collections')

from . import views