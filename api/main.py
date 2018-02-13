from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from models import db, User, Table, Booking
from controllers import BookingController
from functools import wraps
from models_schemas import ma, tables_schema, table_schema, users_schema, user_schema, booking_schema, bookings_schema
import bcrypt
import jwt
from config import DevelopmentConfig

app = Flask(__name__)

# Load config file
app.config.from_object(DevelopmentConfig)

# Load database model
db.init_app(app)
ma.init_app(app)

def token_required(role_needed = None):
    def token_real_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not 'x-access-token' in request.headers:
                return jsonify({'message' : 'Token is missing!'}), 401
            token = request.headers['x-access-token']

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
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

            if "persons" in mandatory_parameters:
                if not (1 <= int(req_data["persons"]) <= 20):
                    return jsonify( { 'message': 'We do not book for more than 20 persons.' } ), 400

            if "date" in mandatory_parameters:
                try:
                    bookingDate = datetime.strptime(req_data["date"], app.config["DATE_FORMAT"])
                except:
                    return jsonify({'message': "Date is not valid (YYYY-mm-dd hh:mm)."}), 400

                # We only accept bookings from oclock or half hours.
                minutes = bookingDate.strftime("%M")
                if(minutes not in ["00", "30"]):
                    return jsonify({'message': "Bookings are accepted only from o'clock or half hours"}), 400

                # We do not accept bookings in the past.
                if request.method == 'POST' and datetime.now() > bookingDate:
                    return jsonify({'message': "We do not accept past dates"}), 400

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

@app.route('/bookings/today')
@token_required()
def get_today_bookings(current_user):
    bookingDate = datetime.now()
    bookingDate = bookingDate.replace(hour=20, minute=00)
    bookingManager = BookingController()

    bookings = bookingManager.get_bookings_from_date(bookingDate)
    bookedTables = bookingManager.get_booked_tables(bookings)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookings_json,
            'totalTables': Table.query.count(),
            'bookedTables': bookedTables
        }
    )

@app.route('/bookings')
@token_required()
@check_mandatory_parameters(["date"])
def get_bookings(current_user):
    bookingDate = datetime.strptime(request.args.get('date'), app.config["DATE_FORMAT"])
    bookingManager = BookingController()

    bookings = bookingManager.get_bookings_from_date(bookingDate)
    bookedTables = bookingManager.get_booked_tables(bookings)
    bookings_json = bookings_schema.dump(bookings).data

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookings_json,
            'totalTables': Table.query.count(),
            'bookedTables': bookedTables,
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
@check_mandatory_parameters(["date", "persons"])
@token_required()
def create_booking(current_user):
    req_data = request.get_json(force=True)

    # Create the booking object, without tables.
    bookingDate = datetime.strptime(req_data["date"], app.config["DATE_FORMAT"])
    booking = Booking(creator=current_user, persons=req_data["persons"], booked_at=bookingDate )

    bookingManager = BookingController()

    # Get free tables
    free_tables = bookingManager.get_free_tables(booking)

    # Get bets tables for this booking.
    best_tables = bookingManager.get_best_tables_for_a_booking(free_tables, booking)
    if None == best_tables:
        return jsonify( { 'message': 'There are not that many availables tables' } ), 400

    for table in best_tables:
        booking.tables.append(table)
    db.session.add(booking)
    db.session.commit()

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

    password = req_data["password"].encode('utf-8')
    hashed = user.password.encode('utf-8')
    if bcrypt.checkpw(password, hashed):
        token = jwt.encode({'username' : user.username, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return jsonify({'message': 'User or Password incorrect.'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
