from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from api.models import db, User, Table, Booking
from api.models import DateValidation, DateTimeValidation, DateUnknownTypeValidation, PersonsNumberValidation
from .controllers import BookingController
from functools import wraps
from .models_schemas import ma, tables_schema, table_schema, users_schema, user_schema, booking_schema, bookings_schema
import bcrypt
import jwt
from .config import DevelopmentConfig, ProductionConfig
import os
import sys
from flask_migrate import Migrate
from flask_cors import CORS


# Check enviroment value
enviroment_mode = os.getenv('SERVER_ENV', None)
if not enviroment_mode:
    print("SERVER_ENV value is missing, setting Development by default.")
    enviroment_mode = "Development"

if enviroment_mode not in ["Production", "Development"]:
    print ("SERVER_ENV value is invalid.")
    sys.exit(0)


app = Flask(__name__)
CORS(app)
env_object = globals()[enviroment_mode + "Config"]
app.config.from_object(env_object)

# Load database model
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

def token_required(role_needed = None):
    def token_real_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
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

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Object not found.'}), 404

@app.route('/')
def index():
    return jsonify({'message': "Wellcome to restaurant API."})

@app.route('/users')
@token_required('Admin')
def get_users(current_user):
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route('/users/me/bookings')
@token_required()
def get_user_bookings(current_user):
    bookingManager = BookingController()
    bookings = bookingManager.get_bookings_from_user(current_user)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'bookings': bookings_json,
            'current_user': current_user.name
        }
    )

@app.route('/users/<int:user_id>')
@token_required('Admin')
def get_user_id(current_user, user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_required('Admin')
def remove_user_id(current_user, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted.'})



@app.route('/users/me')
@token_required()
def get_user_me(current_user):
    return user_schema.jsonify(current_user)



@app.route('/tables')
def get_tables():
    tables = Table.query.all()
    return tables_schema.jsonify(tables)

@app.route('/tables/<int:table_id>')
def get_table_id(table_id):
    table = Table.query.get_or_404(table_id)
    return table_schema.jsonify(table)

@app.route('/bookings')
@token_required()
@check_mandatory_parameters(["date"])
def get_bookings(current_user):
    try:
        dateValidator = DateUnknownTypeValidation(request.args.get('date'), app.config)
        dateValidator.validate()
        bookingDate = dateValidator.date
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    bookingManager = BookingController()
    bookings = bookingManager.get_bookings_from_date(bookingDate)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookings_json,
            'totalTables': Table.query.count(),
            'current_user': current_user.name
        }
    )

@app.route('/bookings/<int:booking_id>')
@token_required()
def get_booking_id(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return booking_schema.jsonify(booking)

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
@token_required('Admin')
def remove_booking_id(current_user, booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted.'})

@app.route('/bookings', methods=['POST'])
@check_mandatory_parameters(["date", "persons", "name"])
@token_required()
def create_booking(current_user):
    req_data = request.get_json(force=True)

    # We accept datetime format only
    try:
        dateValidator = DateTimeValidation(req_data["date"], app.config)
        dateValidator.validate(validatePastRule = True)
        bookingDate = dateValidator.date

        personsValidator = PersonsNumberValidation(req_data["persons"])
        personsValidator.validate()
        persons = personsValidator.persons
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    # Create the booking object, without tables.
    booking = Booking(creator=current_user, persons=persons, booked_at=bookingDate, name=req_data["name"] )

    bookingManager = BookingController()
    try:
        bookingManager.save_booking(booking)
    except Exception  as e:
        return jsonify( { 'message': str(e) } ), 400

    return jsonify(
        {
        'status': 'OK',
        'booking': booking_schema.dump(booking).data
        }
    )

@app.route('/login', methods=['POST'])
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


if __name__ == '__main__':
    app.run(port=app.config["PORT"])
