from flask_marshmallow import Marshmallow
from .models import User, Table, Booking

ma = Marshmallow()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(exclude=['password'], many=True)

class TableSchema(ma.ModelSchema):
    class Meta:
        model = Table

table_schema = TableSchema()
tables_schema = TableSchema(many=True)

class BookingSchema(ma.ModelSchema):
    class Meta:
        model = Booking

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
