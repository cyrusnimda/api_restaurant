from main import app
import unittest

class BookingTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    def test_booking_route(self):
        response = self.tester.get("/bookings")
        self.assertEqual(response.status_code, 200)

    def test_correct_datetime(self):
        response = self.tester.get("/bookings?date=2018-1-1 12:00")
        self.assertEqual(response.status_code, 200)

        response = self.tester.get("/bookings?date=2018-01-01 12:00")
        self.assertEqual(response.status_code, 200)

    def test_incorrect_datetime(self):
        response = self.tester.get("/bookings?date=not_valid")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1 12:12")
        self.assertEqual(response.status_code, 400)

        response = self.tester.get("/bookings?date=2018-1-1 12:12:00")
        self.assertEqual(response.status_code, 400)


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

if __name__ == '__main__':
    unittest.main()
