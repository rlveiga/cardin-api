from flask import jsonify, Blueprint
from app import db
from app.models import User
from . import main

@main.route('/users/', methods=['GET'])
def index():
    users = User.query.all()
    user_list = []

    for u in users:
        user_list.append(u.serialize())

    res = {
        'users': user_list
    }

    return jsonify(res)