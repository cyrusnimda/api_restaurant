from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(200))
    user = db.relationship("User", back_populates="role")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    role = db.relationship("UserRole", back_populates="user")
    bookings = db.relationship('Booking', back_populates='creator')


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
