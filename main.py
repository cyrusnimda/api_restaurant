from flask import Flask, jsonify, request
from datetime import datetime
from models import db, UserRole, User, Table, Booking

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')
print "Config file loaded."

# Load database model
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    users = User.query.all()
    usersJSON = []
    for user in users:
        usersJSON.append(user.json())
    return jsonify({'users': usersJSON})

@app.route('/booking')
def get_bookings():
    bookingDate = request.args.get('date')
    if bookingDate is None:
        bookingDate = datetime.now().strftime('%Y-%m-%d')

    # get booking rate for requested date
    totalTables = Table.query.count()

    bookings = Booking.query.filter(Booking.booked_at.startswith(bookingDate)).all()
    bookingsJSON = []
    bookedTables = 0
    for booking in bookings:
        bookingsJSON.append(booking.json())
        bookedTables = bookedTables + len(booking.tables)

    return jsonify(
        {
            'date': bookingDate,
            'bookings': bookingsJSON,
            'totalTables': totalTables,
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
