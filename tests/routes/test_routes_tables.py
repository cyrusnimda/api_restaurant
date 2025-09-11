import unittest
from tests.base import BaseTestCase
import json


class TableTests(BaseTestCase):

    def test_table_route(self):
        self.start_database()
        response = self.client.get("/tables")
        self.assert200(response)

    def test_table_by_id(self):
        self.start_database()
        response = self.client.get("/tables/1")
        self.assert200(response)

    def test_number_of_tables(self):
        self.start_database()
        response = self.client.get("/tables")
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(len(json_response), 10)

    def test_table_not_found(self):
        self.start_database()
        response = self.client.get("/tables/a")
        self.assert404(response)

        response = self.client.get("/tables/999999")
        self.assert404(response)

if __name__ == '__main__':
    unittest.main()
