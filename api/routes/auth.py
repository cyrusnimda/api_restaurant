from flask import Blueprint, jsonify, request
from api.models import User
from api.decorators import check_mandatory_parameters
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


router = Blueprint("auth", __name__, url_prefix="/login")



@router.route('', methods=['POST'])
@check_mandatory_parameters(["username", "password"])
def login():
    req_data = request.get_json(force=True)
    user = User.query.filter_by(username=req_data["username"]).first()

    if not user:
        return jsonify({'message': 'User or Password incorrect.'}), 401

    password = bytes(req_data["password"], 'utf-8')
    hashed = bytes(user.password, 'utf-8')
    if bcrypt.checkpw(password, hashed):
        token = jwt.encode({'username' : user.username, 'exp' : datetime.now(timezone.utc) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token' : token})

    return jsonify({'message': 'User or Password incorrect.'}), 401