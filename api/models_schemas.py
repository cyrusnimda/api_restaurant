from flask_marshmallow import Marshmallow
from .models import UserRole, User, Table, Booking

ma = Marshmallow()

class UserRoleSchema(ma.ModelSchema):
    class Meta:
        model = UserRole

userrole_schema = UserRoleSchema(exclude=['user', 'desc', 'id'])

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
    role = ma.Nested(userrole_schema)

user_schema = UserSchema(exclude=['password', 'bookings'])
user_schema_only_name = UserSchema(only=['name'])
users_schema = UserSchema(exclude=['password', 'bookings'], many=True)

class TableSchema(ma.ModelSchema):
    class Meta:
        model = Table

table_schema = TableSchema()
tables_schema = TableSchema(many=True)

class BookingSchema(ma.ModelSchema):
    class Meta:
        model = Booking
    creator = ma.Nested(user_schema_only_name)

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
