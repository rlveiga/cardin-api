from flask import Blueprint

collection = Blueprint('collection', __name__, url_prefix='/collections')
owned_collection = Blueprint('owned_collection', __name__, url_prefix='/owned_collections')

from . import views