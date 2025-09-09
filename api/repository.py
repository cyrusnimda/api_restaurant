from api.models import Restaurant, db, Table, Booking, User, UserRole
import bcrypt
from api.feeds.restaurants import restaurants_data

def db_feeds(db):
    with db.session.begin():
        # Add Roles
        admin = UserRole(name='Admin', desc='App admin')
        manager = UserRole(name='Manager', desc='Restaurant manager')
        employee = UserRole(name='Employee', desc='Restaurant employee')
        customer = UserRole(name='Customer', desc='Restaurant customer')

        admin_exists = UserRole.query.filter_by(name='Admin').first()
        if not admin_exists:
            db.session.add(admin)
            db.session.add(manager)
            db.session.add(employee)
            db.session.add(customer)

        # Add users
        josu_bcrypt_pass = bcrypt.hashpw(b'josupass', bcrypt.gensalt()).decode('utf-8')
        josu = User(name='Josu Ruiz', username='josu', password=josu_bcrypt_pass, role=admin)
        maria_bcrypt_pass = bcrypt.hashpw(b'mariapass', bcrypt.gensalt()).decode('utf-8')
        maria = User(name='Maria Ruiz', username='maria', password=maria_bcrypt_pass, role=customer)

        josu_exists = User.query.filter_by(username='josu').first()
        if not josu_exists:
            db.session.add(josu)
            db.session.add(maria)

        # Add restaurants
        for r in restaurants_data:
            exists = Restaurant.query.filter_by(name=r["name"]).first()
            if not exists:
                restaurant = Restaurant(**r)
                db.session.add(restaurant)

        db.session.commit()