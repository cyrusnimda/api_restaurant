from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')
print "Config file loaded."

# Load database model
db = SQLAlchemy(app)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(200))
    user = db.relationship("User", back_populates="role")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    token = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    role = db.relationship("UserRole", back_populates="user")
    bookings = db.relationship('Booking', back_populates='creator', lazy=True)

    def json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "role" : self.role.name
        }

booking_tables = db.Table('booking_tables',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id'), primary_key=True),
    db.Column('booking_id', db.Integer, db.ForeignKey('booking.id'), primary_key=True)
)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200))
    seats = db.Column(db.Integer)

    def json(self):
        return {
            "id" : self.id,
            "desc": self.desc,
            "seats" : self.seats
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booked_at = db.Column(db.DateTime)
    tables = db.relationship('Table', secondary=booking_tables, lazy='subquery')
    persons = db.Column(db.Integer)
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", back_populates="bookings")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        jsonBooking = {
            "id" : self.id,
            "booked_at" : self.booked_at.strftime('%Y-%m-%d %H:%M'),
            "persons" : self.persons,
            "created_at" : self.created_at.strftime('%Y-%m-%d %H:%M'),
            "creator": self.creator.json()
        }
        tablesArray = []
        for table in self.tables:
            tablesArray.append(table.json())
        jsonBooking["tables"] = tablesArray

        return jsonBooking

#Load init data in database
if app.config["ADD_INITIAL_DATA"] == True:
    # remove file if exists
    import os.path
    import sys
    file = "./database/restaurant.db"
    database_exists = os.path.isfile(file)
    if database_exists:
        os.remove(file)

    db.create_all()
    print "Database models created."

    admin = UserRole(name='Admin', desc='App admin')
    manager = UserRole(name='Manager', desc='Restaurant manager')
    employee = UserRole(name='Employee', desc='Restaurant employee')
    customer = UserRole(name='Customer', desc='Restaurant customer')
    db.session.add(admin)
    db.session.add(manager)
    db.session.add(employee)
    db.session.add(customer)

    josu = User(name='Josu', password='josupass', role=admin)
    maria = User(name='Maria', password='mariapass', role=customer)
    db.session.add(josu)
    db.session.add(maria)

    table1 = Table(desc='Table closest to front door', seats=4)
    table2 = Table(seats=2)
    table3 = Table(desc='Circular table', seats=8)
    db.session.add(table1)
    db.session.add(table2)
    db.session.add(table3)

    booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
    booking.tables.append(table1)
    booking.tables.append(table2)
    db.session.add(booking)

    db.session.commit()
    print "Init data created in database"


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

@app.route('/bookings')
def get_bookings():
    bookingDate = request.args.get('date')
    if bookingDate is None:
        bookingDate = datetime.now().strftime('%Y-%m-%d')

    bookings = Booking.query.filter(Booking.booked_at.startswith(bookingDate)).all()
    bookingsJSON = []
    for booking in bookings:
        bookingsJSON.append(booking.json())

    return jsonify({'date': bookingDate,'bookings': bookingsJSON})


if __name__ == '__main__':
    app.run()
