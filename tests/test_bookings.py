import unittest
from base import BaseTestCase
import json
from api.models import db, Table, Booking, User, UserRole
from api.controllers import BookingController
from datetime import datetime
import copy

class BookingControllerTests(BaseTestCase):

    def test_delete_booking_admin(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.delete("/bookings/1", headers=self.headers)
        self.assert200(response)
        response = self.client.get("/bookings/1", headers=self.headers)
        self.assert404(response)

    def test_delete_booking_no_admin(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token('maria','mariapass')}
        response = self.client.delete("/bookings/1", headers=self.headers)
        self.assert403(response)

    def test_get_correct_date(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings?date=2018-1-1 14:00", headers=self.headers)
        json_response = json.loads(response.data)
        self.assert200(response)

        response = self.client.get("/bookings?date=2018-01-01 14:00", headers=self.headers)
        json_response = json.loads(response.data)
        self.assert200(response)

    def test_number_of_bookings(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings?date=2018-1-1 14:00", headers=self.headers)
        json_response = json.loads(response.data)
        self.assertEqual(len(json_response["bookings"]), 2)

    def test_get_best_tables(self):
        with self.app.app_context():
            tables = Table.query.order_by(Table.seats).all()
            josu = User.query.filter_by(name="josu").first()
        bookingManager = BookingController()

        booking = Booking(creator=josu, persons=10, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 2)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 2 )

        booking = Booking(creator=josu, persons=3, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)

        booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 10)

        booking = Booking(creator=josu, persons=20, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(tables), booking)
        self.assertEqual(len(best_tables), 4)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 10)
        self.assertEqual( best_tables[2].id, 9)
        self.assertEqual( best_tables[3].id, 2)

        with self.app.app_context():
            table = Table.query.get(1)
        booking = Booking(creator=josu, persons=20, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking([table], booking)
        self.assertIsNone(best_tables)

        with self.app.app_context():
            table = Table.query.get(1)
        booking = Booking(creator=josu, persons=4, booked_at=datetime.strptime("2018-01-30 20:00", self.app.config["DATE_FORMAT"]) )
        best_tables = bookingManager.get_best_tables_for_a_booking([table], booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)


if __name__ == '__main__':
    unittest.main()
