import unittest
from base import BaseTestCase


class TableTests(BaseTestCase):

    def test_table_route(self):
        response = self.client.get("/tables")
        self.assert200(response)

        response = self.client.get("/tables/1")
        self.assert200(response)

    def test_table_not_found(self):
        response = self.client.get("/tables/a")
        self.assert404(response)

        response = self.client.get("/tables/999999")
        self.assert404(response)

if __name__ == '__main__':
    unittest.main()
