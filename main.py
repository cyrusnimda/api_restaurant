from flask import Flask, jsonify, request
from datetime import datetime
from models import db, UserRole, User, Table, Booking

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')

# Load database model
db.init_app(app)

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

@app.route('/booking')
def get_bookings():
    bookingDateStr = request.args.get('date')
    dateFormat = "%Y-%m-%d %H:%M"

    if bookingDateStr is None:
        bookingDate = datetime.now()
        bookingDate = bookingDate.replace(hour=20, minute=00)
    else:
        try:
            bookingDate = datetime.strptime(bookingDateStr, dateFormat)
        except:
            return jsonify({'message': "Date is not valid (YYYY-mm-dd hh:mm)."}), 301
        # We only accept bookings from oclock or half hours.
        hour = bookingDate.strftime("%M")
        if(hour not in ["00", "30"]):
            return jsonify({'message': "Bookings are accepted only from o'clock or half hours"}), 301

    bookings = Booking.query.filter(Booking.booked_at.startswith( bookingDate.strftime(dateFormat) )).all()
    bookingsJSON = []
    bookedTables = 0
    for booking in bookings:
        bookingsJSON.append(booking.json())
        bookedTables = bookedTables + len(booking.tables)

    return jsonify(
        {
            'date': bookingDate.strftime(dateFormat),
            'bookings': bookingsJSON,
            'totalTables': Table.query.count(),
            'bookedTables': bookedTables
        }
    )

@app.route('/booking', methods=['POST'])
def create_booking():
    req_data = request.get_json(force=True)
    if not req_data:
        return jsonify( { 'Error': 'No JSON found' } )

    print req_data["persons"]
    booking = Booking(creator=josu, persons=req_data["persons"], booked_at=req_data["booked_at"] )
    error = booking.validate()


    return jsonify( { 'status': 'OK' } )


if __name__ == '__main__':
    app.run()
