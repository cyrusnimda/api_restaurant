import unittest
from api.models import db, Table, Booking, User, UserRole
from api.controllers import BookingController
from datetime import datetime
import copy

class ControllerTests(unittest.TestCase):

    def test_get_best_tables(self):
        self.sample_date = datetime.strptime("2018-01-30 20:00", "%Y-%m-%d %H:%M")

        mock_tables = [
            Table(id=1, seats=4),
            Table(id=2, seats=2),
            Table(id=3, seats=8),
            Table(id=4, seats=2),
            Table(id=5, seats=2),
            Table(id=6, seats=4),
            Table(id=7, seats=4),
            Table(id=8, seats=4),
            Table(id=9, seats=4),
            Table(id=10, seats=6),
        ]
        admin = UserRole(name='Admin', desc='App admin')
        josu = User(name='Josu Ruiz', username='josu', password="xxxxx", role=admin)
        mock_tables.sort(key=lambda x: x.seats, reverse=False)
        bookingManager = BookingController()

        booking = Booking(creator=josu, persons=10, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(mock_tables), booking)
        self.assertEqual(len(best_tables), 2)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 2)

        booking = Booking(creator=josu, persons=3, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(mock_tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)

        booking = Booking(creator=josu, persons=5, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(mock_tables), booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 10)

        booking = Booking(creator=josu, persons=20, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking(copy.deepcopy(mock_tables), booking)
        self.assertEqual(len(best_tables), 4)
        self.assertEqual( best_tables[0].id, 3)
        self.assertEqual( best_tables[1].id, 10)
        self.assertEqual( best_tables[2].id, 9)
        self.assertEqual( best_tables[3].id, 2)

        booking = Booking(creator=josu, persons=20, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking([copy.deepcopy(mock_tables)[3]], booking)
        self.assertIsNone(best_tables)

        booking = Booking(creator=josu, persons=4, booked_at=self.sample_date )
        best_tables = bookingManager.get_best_tables_for_a_booking([copy.deepcopy(mock_tables)[3]], booking)
        self.assertEqual(len(best_tables), 1)
        self.assertEqual( best_tables[0].id, 1)


if __name__ == '__main__':
    unittest.main()
