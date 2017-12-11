#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ARMUmysqlr00t@127.0.0.1/restaurant'

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(200))
    users = db.relationship('Booking', backref='role', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    token = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    bookings = db.relationship('Booking', backref='creator', lazy=True)

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
    datetime = db.Column(db.DateTime)
    tables = db.relationship('Table', secondary=booking_tables, lazy='subquery')
    persons = db.Column(db.Integer)
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime)
