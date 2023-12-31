import unittest
from tests.base import BaseTestCase
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

    
if __name__ == '__main__':
    unittest.main()
