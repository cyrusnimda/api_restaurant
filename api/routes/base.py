from flask import Blueprint, jsonify

router = Blueprint("base", __name__, url_prefix="/")

@router.route('/')
def index():
    return jsonify({'message': "Wellcome to restaurant API."})