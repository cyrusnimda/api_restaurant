from main import app
import unittest
import json
from flask import Flask
from models import db, Table, Booking, User, UserRole
from controllers import BookingController
from datetime import datetime
import copy

class BookingTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_correct_date(self):
        response = self.tester.get("/bookings?date=2018-1-1 12:00")
        self.assertEqual(response.status_code, 200)

        response = self.tester.get("/bookings?date=2018-01-01 12:00")
        self.assertEqual(response.status_code, 200)

    def test_get_incorrect_date(self):
        response = self.tester.get("/bookings")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=not_valid")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1 12:12")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1 12:12:00")
        self.assertEqual(response.status_code, 400)

    def test_post_empty_booking_route(self):
        response = self.tester.post("/bookings")
        self.assertEqual(response.status_code, 400)

    def test_post_mandatory_parameter_missing_booking_route(self):
        data = {'persons': 4}
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {'date': '2018-01-30 17:00'}
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_correct_booking_route(self):
        data = {
            'persons': 1,
            'date': '2018-01-30 17:00'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = {
            'persons': '20',
            'date': '2018-01-30 17:00'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_error_persons_route(self):
        data = {
            'persons': 24,
            'date': '2018-01-30 17:00'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'persons': 0,
            'date': '2018-01-30 17:00'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_error_date_route(self):
        data = {
            'persons': 4,
            'date': '2018-01-30 17:00:00'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'persons': 4,
            'date': '2018-01-30 17:23'
        }
        response = self.tester.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)



class BookingControllerTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

        # Creates a new database for the unit test to use
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['TESTING'] = True
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.populate_db()

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

        josu = User(name='Josu', password='josupass', role=admin)
        maria = User(name='Maria', password='mariapass', role=customer)
        with self.app.app_context():
            db.session.add(josu)
            db.session.add(maria)

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

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_correct_date(self):
        response = self.tester.get("/bookings?date=2018-1-1 14:00")
        json_response = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response["bookings"]), 1)


        response = self.tester.get("/bookings?date=2018-01-01 14:00")
        json_response = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response["bookings"]), 1)

    def test_get_best_tables(self):
        with self.app.app_context():
            tables = Table.query.order_by(Table.seats).all()
            josu = User.query.filter_by(name="josu").first()
        bookingManager = BookingController()

        booking = Booking(creator=josu, persons=10, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 2)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 2 )

        booking = Booking(creator=josu, persons=3, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)

        booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 10)

        booking = Booking(creator=josu, persons=20, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 4)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 10)
        self.assertEqual( best_tables[2].id, 9)
        self.assertEqual( best_tables[3].id, 2)

        with self.app.app_context():
            table = Table.query.get(1)
        booking = Booking(creator=josu, persons=20, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking([table], booking)
        self.assertIsNone(best_tables)

        with self.app.app_context():
            table = Table.query.get(1)
        booking = Booking(creator=josu, persons=4, booked_at=datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M") )
        best_tables = bookingManager.get_best_tables_for_a_booking([table], booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)


class TableTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    def test_table_route(self):
        response = self.tester.get("/tables")
        self.assertEqual(response.status_code, 200)

        response = self.tester.get("/tables/1")
        self.assertEqual(response.status_code, 200)

    def test_table_not_found(self):
        response = self.tester.get("/tables/a")
        self.assertEqual(response.status_code, 404)

        response = self.tester.get("/tables/999999")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
