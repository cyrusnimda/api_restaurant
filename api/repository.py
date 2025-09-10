from api.models import Restaurant, db, Table, Booking, User, UserRole
import bcrypt
from api.feeds.restaurants import restaurants_data
from api.feeds.tables import tables_data
from api.feeds.roles import roles_data
from api.feeds.users import users_data

def db_feeds(db):
    with db.session.begin():
        # Add Roles
        for role in roles_data:
            exists = UserRole.query.filter_by(name=role["name"]).first()
            if not exists:
                new_role = UserRole(**role)
                db.session.add(new_role)

        # Add users
        for user in users_data:
            exists = User.query.filter_by(username=user["username"]).first()
            if not exists:
                user_bcrypt_pass = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                role = UserRole.query.filter_by(id=user["role"]).first()
                new_user = User(name=user["name"], username=user["username"], password=user_bcrypt_pass, role=role)
                db.session.add(new_user)


        # Add restaurants
        for r in restaurants_data:
            exists = Restaurant.query.filter_by(name=r["name"]).first()
            if not exists:
                restaurant = Restaurant(**r)
                db.session.add(restaurant)

        # Add tables
        for table in tables_data:
            exists = Table.query.filter_by(desc=table["desc"]).first()
            if not exists:
                new_table = Table(**table)
                db.session.add(new_table)

        db.session.commit()