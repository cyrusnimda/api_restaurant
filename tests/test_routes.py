import unittest
from base import BaseTestCase
import json

class RoutesTests(BaseTestCase):

    def test_login_get(self):
        response = self.client.get('/login')
        self.assert405(response)

    def test_login_post(self):
        response = self.client.post('/login')
        self.assert400(response)

    def test_database_exits(self):
        data = {'username': 'josu',
                'password': '*******'}
        response = self.client.post("/login",
                              data=json.dumps(data),
                              content_type='application/json')
        json_response = json.loads(response.data.decode('utf-8'))
        message = json_response["message"]
        self.assertEqual("User or Password incorrect.", message)

    def test_login_correct(self):
        data = {'username': 'josu',
                'password': 'josupass'}
        response = self.client.post("/login",
                              data=json.dumps(data),
                              content_type='application/json')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertIn("token", json_response)

    def test_get_correct_date(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings?date=2018-1-1 12:00", headers=self.headers)
        self.assert200(response)

        response = self.client.get("/bookings?date=2018-01-01 12:00", headers=self.headers)
        self.assert200(response)

    def test_get_incorrect_date(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=not_valid", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=2018-1-1", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=2018-1-1 12:12", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=2018-1-1 12:12:00", headers=self.headers)
        self.assert400(response)

    def test_post_empty_booking_route(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.post("/bookings", headers=self.headers)
        self.assert400(response)

    def test_get_today_bookings(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings/today", headers=self.headers)
        self.assert200(response)

    def test_get_today_bookings_without_token(self):
        response = self.client.get("/bookings/today")
        self.assert401(response)

    def test_post_mandatory_parameter_missing_booking_route(self):
        data = {'persons': 4}
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {'date': '2018-01-30 17:00'}
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_correct_booking_route(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 1,
            'date': '2028-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert200(response)

        data = {
            'persons': '20',
            'date': '2028-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              headers=self.headers,
                              content_type='application/json')
        self.assert200(response)

    def test_post_error_persons_integer(self):
        data = {
            'persons': 'a',
            'date': '2018-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 0,
            'date': '2018-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_error_persons_route(self):
        data = {
            'persons': 24,
            'date': '2018-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 0,
            'date': '2018-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_error_date_past(self):
        data = {
            'persons': 1,
            'date': '2015-01-30 17:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_error_date_format(self):
        data = {
            'persons': 4,
            'date': '2018-01-30 17:00:00'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 4,
            'date': '2018-01-30 17:23'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

if __name__ == '__main__':
    unittest.main()
