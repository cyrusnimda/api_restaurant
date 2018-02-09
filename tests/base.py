from flask_testing import TestCase

from api.main import app
from api.models import db, Table, Booking, User, UserRole
from api.config import TestConfig
from datetime import datetime
import bcrypt
import json

class BaseTestCase(TestCase):


    def get_token(self, user='josu', password='josupass'):
        data = {'username': user,
                'password': password}
        response = self.client.post("/login",
                              data=json.dumps(data),
                              content_type='application/json')
        json_response = json.loads(response.data)
        return json_response["token"];

    def create_app(self):
        self.app = app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.populate_db()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        admin = UserRole(name='Admin', desc='App admin')
        manager = UserRole(name='Manager', desc='Restaurant manager')
        employee = UserRole(name='Employee', desc='Restaurant employee')
        customer = UserRole(name='Customer', desc='Restaurant customer')
        with self.app.app_context():
            db.session.add(admin)
            db.session.add(manager)
            db.session.add(employee)
            db.session.add(customer)
            db.session.commit()

        josu = User(name='Josu Ruiz', username='josu', password=bcrypt.hashpw('josupass', bcrypt.gensalt()), role=admin)
        maria = User(name='Maria Lopez', username='maria', password=bcrypt.hashpw('mariapass', bcrypt.gensalt()), role=customer)
        with self.app.app_context():
            db.session.add(josu)
            db.session.add(maria)
            db.session.commit()

        table1 = Table(desc='Table closest to front door', seats=4)
        table2 = Table(desc='Table number 2', seats=2)
        table3 = Table(desc='Circular table', seats=8)
        table4 = Table(desc='Table number 4', seats=2)
        table5 = Table(desc='Table number 5', seats=2)
        table6 = Table(desc='Table number 6', seats=4)
        table7 = Table(desc='Table number 7', seats=4)
        table8 = Table(desc='Table number 8', seats=4)
        table9 = Table(desc='Table number 9', seats=4)
        table10 = Table(desc='Table number 10', seats=6)
        with self.app.app_context():
            db.session.add(table1)
            db.session.add(table2)
            db.session.add(table3)
            db.session.add(table4)
            db.session.add(table5)
            db.session.add(table6)
            db.session.add(table7)
            db.session.add(table8)
            db.session.add(table9)
            db.session.add(table10)
            db.session.commit()

        booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
        booking.tables.append(table1)
        booking.tables.append(table2)
        with self.app.app_context():
            db.session.add(booking)
            db.session.commit()
