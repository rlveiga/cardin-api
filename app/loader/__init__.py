from flask import Blueprint

loader = Blueprint('loader', __name__, url_prefix='/loaderio-824546430810ec9656e2257ba7f15059')

from . import views