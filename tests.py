from main import app
import unittest

class BookingTests(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        
    def test_booking_route(self):
        response = self.tester.get("/booking")
        self.assertEqual(response.status_code, 200)

    def test_correct_datetime(self):
        response = self.tester.get("/booking?date=2018-1-1 12:00")
        self.assertEqual(response.status_code, 200)

        response = self.tester.get("/booking?date=2018-01-01 12:00")
        self.assertEqual(response.status_code, 200)

    def test_incorrect_datetime(self):
        response = self.tester.get("/booking?date=not_valid")
        self.assertEqual(response.status_code, 301)

        response = self.tester.get("/booking?date=2018-1-1")
        self.assertEqual(response.status_code, 301)

        response = self.tester.get("/booking?date=2018-1-1 12:12")
        self.assertEqual(response.status_code, 301)

        response = self.tester.get("/booking?date=2018-1-1 12:12:00")
        self.assertEqual(response.status_code, 301)




if __name__ == '__main__':
    unittest.main()
