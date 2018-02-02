from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from models import db, UserRole, User, Table, Booking
from controllers import BookingController
from functools import wraps

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')

# Load database model
db.init_app(app)


def check_mandatory_parameters(mandatory_parameters):
    def real_decorator(original_function):
        @wraps(original_function)
        def wrapper_function():
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

            return original_function()
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
    usersJSON = []
    for user in users:
        usersJSON.append(user.json())
    return jsonify({'users': usersJSON})

@app.route('/tables')
def get_tables():
    tables = Table.query.all()
    tablesJSON = []
    for table in tables:
        tablesJSON.append(table.json())
    return jsonify({'tables': tablesJSON})

@app.route('/tables/<int:table_id>')
def get_table_id(table_id):
    table = Table.query.get_or_404(table_id)
    return jsonify({'table': table.json()})

@app.route('/bookings/today')
def get_today_bookings():    
    bookingDate = datetime.now()
    bookingDate = bookingDate.replace(hour=20, minute=00)
    bookings = Booking.query.filter(Booking.booked_at.startswith( bookingDate.strftime(app.config["DATE_FORMAT"]) )).all()

    bookingsJSON = []
    bookedTables = 0
    for booking in bookings:
        bookingsJSON.append(booking.json())
        bookedTables = bookedTables + len(booking.tables)

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookingsJSON,
            'totalTables': Table.query.count(),
            'bookedTables': bookedTables
        }
    )
@app.route('/bookings')
@check_mandatory_parameters(["date"])
def get_bookings():
    bookingDate = datetime.strptime(request.args.get('date'), app.config["DATE_FORMAT"])
    bookings = Booking.query.filter(Booking.booked_at.startswith( bookingDate.strftime(app.config["DATE_FORMAT"]) )).all()

    bookingsJSON = []
    bookedTables = 0
    for booking in bookings:
        bookingsJSON.append(booking.json())
        bookedTables = bookedTables + len(booking.tables)

    return jsonify(
        {
            'date': bookingDate.strftime(app.config["DATE_FORMAT"]),
            'bookings': bookingsJSON,
            'totalTables': Table.query.count(),
            'bookedTables': bookedTables
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


if __name__ == '__main__':
    app.run()
