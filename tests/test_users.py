import unittest
from base import BaseTestCase


class UserTests(BaseTestCase):

    def test_see_all_users_without_token(self):
        response = self.client.get("/users")
        self.assert401(response)

    def test_see_all_users_without_admin(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token('maria','mariapass')}
        response = self.client.get("/users", headers=self.headers)
        self.assert403(response)

    def test_see_all_users(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/users", headers=self.headers)
        self.assert200(response)

    def test_see_my_user(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/user/me", headers=self.headers)
        self.assert200(response)

    def test_see_current_user(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/user/1", headers=self.headers)
        self.assert200(response)

    def test_see_other_user(self):
        self.headers = {'Content-Type': 'application/json', 'x-access-token': self.get_token()}
        response = self.client.get("/user/2", headers=self.headers)
        self.assert403(response)

if __name__ == '__main__':
    unittest.main()
