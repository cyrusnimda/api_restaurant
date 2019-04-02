import unittest
from tests.base import BaseTestCase
import json

class RoutesBookingsTests(BaseTestCase):

    def test_get_correct_date(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings?date=2018-1-1 12:00", headers=self.headers)
        self.assert200(response)

        response = self.client.get("/bookings?date=2018-01-01 19:30", headers=self.headers)
        self.assert200(response)

        response = self.client.get("/bookings?date=2018-1-1", headers=self.headers)
        self.assert200(response)

        response = self.client.get("/bookings?date=2018-01-01", headers=self.headers)
        self.assert200(response)

    def test_get_incorrect_date(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=not_valid", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=2018-1-1 12:12", headers=self.headers)
        self.assert400(response)

        # Not in BOOKING_HOURS config
        response = self.client.get("/bookings?date=2018-01-01 10:00", headers=self.headers)
        self.assert400(response)

        response = self.client.get("/bookings?date=2018-1-1 12:12:00", headers=self.headers)
        self.assert400(response)

    def test_post_empty_booking_route(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.post("/bookings", headers=self.headers)
        self.assert400(response)

    def test_post_mandatory_parameter_missing_booking_route(self):
        data = {'persons': 4}
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {'date': '2018-01-30 19:00'}
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_correct_booking_route(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 1,
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                              headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert200(response)

        data = {
            'persons': '20',
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              headers=self.headers,
                              content_type='application/json')
        self.assert200(response)

        self.restart_database()

    def test_post_error_empty_name(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 'a',
            'date': '2218-01-30 19:00'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)


    def test_post_error_persons_integer(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 'a',
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 0,
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                              data=json.dumps(data),
                              headers=self.headers,
                              content_type='application/json')
        self.assert400(response)

    def test_post_error_persons_route(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 24,
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 0,
            'date': '2218-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,    
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_post_error_date_past(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 1,
            'date': '2015-01-30 19:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)
 

    def test_post_error_date_format(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        data = {
            'persons': 4,
            'date': '2218-01-30 17:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                            data=json.dumps(data),
                            content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 4,
            'date': '2218-01-30 19:00:00',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

        data = {
            'persons': 4,
            'date': '2218-01-30 19:23',
            'name' : 'Paco'
        }
        response = self.client.post("/bookings",
                            headers=self.headers,
                              data=json.dumps(data),
                              content_type='application/json')
        self.assert400(response)

    def test_delete_booking_admin(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.delete("/bookings/1", headers=self.headers)
        self.assert200(response)
        response = self.client.get("/bookings/1", headers=self.headers)
        self.assert404(response)

        self.restart_database()


    def test_delete_booking_no_admin(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token('maria','mariapass')}
        response = self.client.delete("/bookings/1", headers=self.headers)
        self.assert403(response)

    def test_number_of_bookings(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/bookings?date=2018-1-1 14:00", headers=self.headers)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(json_response["bookings"]), 2)

        response = self.client.get("/bookings?date=2018-1-1", headers=self.headers)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(json_response["bookings"]), 3)



if __name__ == '__main__':
    unittest.main()
