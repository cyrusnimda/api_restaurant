from main import app
import unittest
import json

class BookingTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_booking_route(self):
        response = self.tester.get("/bookings")
        self.assertEqual(response.status_code, 200)

    def test_get_correct_date(self):
        response = self.tester.get("/bookings?date=2018-1-1 12:00")
        self.assertEqual(response.status_code, 200)

        response = self.tester.get("/bookings?date=2018-01-01 12:00")
        self.assertEqual(response.status_code, 200)

    def test_get_incorrect_date(self):
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
            'persons': 20,
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
