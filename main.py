from flask import Flask
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

booking_tables = db.Table('booking_tables',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id'), primary_key=True),
    db.Column('booking_id', db.Integer, db.ForeignKey('booking.id'), primary_key=True)
)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200))
    seats = db.Column(db.Integer)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booked_at = db.Column(db.DateTime)
    tables = db.relationship('Table', secondary=booking_tables, lazy='subquery')
    persons = db.Column(db.Integer)
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship("User", back_populates="bookings")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all();
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


if __name__ == '__main__':
    app.run()
