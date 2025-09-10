from functools import wraps
import os
from flask import request, jsonify, current_app as app
import jwt
from api.models import User


def token_required(role_needed = None):
    def token_real_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            enviroment_mode = os.getenv('SERVER_ENV', 'Development')

            if not 'x-access-token' in request.headers:
                return jsonify({'message' : 'Token is missing!'}), 401
            token = request.headers['x-access-token']
            try:
                if enviroment_mode == "Development" and token == "postman_dev_key_1928465":
                    current_user = User.query.filter_by(username="josu").first()
                else:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                    current_user = User.query.filter_by(username=data['username']).first()

                if role_needed and role_needed != current_user.role.name:
                    return jsonify({'message': 'Permission denied.'}), 403
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    return token_real_decorator


def check_mandatory_parameters(mandatory_parameters):
    def real_decorator(original_function):
        @wraps(original_function)
        def wrapper_function(*args, **kwargs):
            if request.method == 'POST':
                req_data = request.get_json(force=True)
            elif request.method == 'GET':
                req_data = request.args

            if not req_data:
                return jsonify( { 'message': 'No parameters found.' } ), 400

            for parameter in mandatory_parameters:
                if parameter not in req_data:
                    return jsonify( { 'message': '"{}" is a mandatory parameter.'.format(parameter) } ), 400
            
            return original_function(*args, **kwargs)
        return wrapper_function
    return real_decorator

