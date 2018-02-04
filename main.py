from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from models import db, User, Table, Booking
from controllers import BookingController
from functools import wraps
from models_schemas import ma, tables_schema, table_schema, users_schema, user_schema, booking_schema, bookings_schema
import bcrypt
import jwt

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')

# Load database model
db.init_app(app)
ma.init_app(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

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
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route('/tables')
def get_tables():
    tables = Table.query.all()
    return tables_schema.jsonify(tables)

@app.route('/tables/<int:table_id>')
def get_table_id(table_id):
    table = Table.query.get_or_404(table_id)
    return table_schema.jsonify(table)

@app.route('/bookings/today')
def get_today_bookings():
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
@token_required
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

@app.route('/bookings', methods=['POST'])
@check_mandatory_parameters(["date", "persons"])
def create_booking():
    req_data = request.get_json(force=True)

    # Create the booking object, without tables.
    josu = User.query.filter_by(name="josu").first()
    bookingDate = datetime.strptime(req_data["date"], app.config["DATE_FORMAT"])
    booking = Booking(creator=josu, persons=req_data["persons"], booked_at=bookingDate )

    bookingManager = BookingController()

    # Get free tables
    free_tables = bookingManager.get_free_tables(booking)

    # Get bets tables for this booking.
    best_tables = bookingManager.get_best_tables_for_a_booking(free_tables, booking)

    return jsonify( { 'status': 'OK' } )

@app.route('/login', methods=['POST'])
@check_mandatory_parameters(["username", "password"])
def login():
    req_data = request.get_json(force=True)
    user = User.query.filter_by(username=req_data["username"]).first()

    if not user:
        return jsonify({'message': 'Could not verify.'}), 401

    #hashed = bcrypt.hashpw(req_data["password"].encode('utf-8'), bcrypt.gensalt())
    if bcrypt.hashpw(req_data["password"].encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
        #token = jwt.encode({'username' : user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        token = jwt.encode({'username' : user.username, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return jsonify({'message': 'User or Password incorrect.'}), 401


if __name__ == '__main__':
    app.run()
