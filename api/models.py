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
    bookings = db.relationship('Booking', back_populates='creator', cascade="all,delete")


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
    persons = db.Column(db.Integer)
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50))
    
    tables = db.relationship('Table', secondary=booking_tables, lazy='subquery')
    creator = db.relationship("User", back_populates="bookings")

class Validation():
    def validate(self):
        print("Validating...")

class PersonsNumberValidation(Validation):
    def __init__(self, stringPersonsNumber):
        self.stringPersonsNumber = stringPersonsNumber
        self.convert_to_object()

    def convert_to_object(self):
        try:
            self.persons = int(self.stringPersonsNumber)
        except:
            raise ValueError('Invalid persons number.')
    
    def validate(self):
        if not (1 <= self.persons <= 20):
            raise ValueError('We do not book for more than 20 persons.')
        return True

class DateBaseValidation(Validation):
    date = None

    def __init__(self, stringDate, config):
        self.stringDate = stringDate
        self.config = config
        self.convert_to_object()

    def validate(self, validatePastRule = False):
        self.check_oclock_rule()
        if validatePastRule:
            self.check_past_rule()
        return True

    def convert_to_object(self):
        print("Converting StringDate in DateObject...")
    
    def check_past_rule(self):
        # We do not accept bookings in the past.
        if datetime.now() > self.date:
            raise ValueError('We do not accept past dates.')
    
    def check_oclock_rule(self):
        #We only accept booking in BOOKING_HOURS setting var
        hour = self.date.strftime("%H:%M")
        # 00:00 means is a whole day date, not need for checking hours.
        if hour != "00:00" and hour not in self.config["BOOKING_HOURS"]:
            raise ValueError('We only accept bookings in some hours.')

# Date format validation "2018-01-01"
class DateValidation(DateBaseValidation):
    def convert_to_object(self):
        try:
            self.date = datetime.strptime(self.stringDate, "%Y-%m-%d")
        except:
            raise ValueError('Date is not valid (YYYY-mm-dd hh:mm).')

# Datetime format validation "2018-01-01 12:25"
class DateTimeValidation(DateBaseValidation):
    def convert_to_object(self):
        try:
            self.date = datetime.strptime(self.stringDate, self.config["DATE_FORMAT"])
        except:
            raise ValueError('Date is not valid (YYYY-mm-dd hh:mm).')

# Some requests accept both formats, date and datetime, so we need to validate 
# For both of them.
class DateUnknownTypeValidation(DateBaseValidation):
    def convert_to_object(self):
        try:
            self.date = datetime.strptime(self.stringDate, "%Y-%m-%d")
        except:
            try:
                self.date = datetime.strptime(self.stringDate, self.config["DATE_FORMAT"])
            except:
                ValueError('Date format is not valid.')
            