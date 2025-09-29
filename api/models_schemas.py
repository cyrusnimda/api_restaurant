from flask_marshmallow import Marshmallow
from .models import Restaurant, UserRole, User, Table, Booking

ma = Marshmallow()

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant
        load_instance = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        load_instance = True

    user = ma.Nested('UserSchema', exclude=['role'])
userrole_schema = UserRoleSchema(exclude=['desc', 'id'])

#userrole_schema = UserRoleSchema(exclude=['user', 'desc', 'id'])


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    role = ma.Nested(userrole_schema)
    bookings = ma.Nested('BookingSchema', many=True)

user_schema = UserSchema(exclude=['password', 'bookings'])
user_schema_only_name = UserSchema(only=['name'])
users_schema = UserSchema(exclude=['password', 'bookings'], many=True)

class TableSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Table
        load_instance = True

table_schema = TableSchema()
tables_schema = TableSchema(many=True)

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
    creator = ma.Nested(user_schema_only_name)
    tables = ma.Nested(table_schema, many=True)

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
