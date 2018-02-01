from datetime import datetime, timedelta
from models import Table, Booking

class BookingController():

    def _get_best_table(self, tables, persons, assigned_tables):
        while persons > 0 and len(tables) > 0:
            for index, table in enumerate(tables):
                if persons <= table.seats or len(tables) -1 == index:
                    tables.remove(table)
                    persons = int(persons) - table.seats
                    assigned_tables.append(table)
                    break
        return assigned_tables


    def get_best_tables_for_a_booking(self, tables, booking):
        persons = booking.persons
        best_tables = self._get_best_table(tables, persons, [])
        return best_tables

    def get_free_tables(self, booking):
        dateFormat = "%Y-%m-%d %H:%M"

        # Booking are for 1 hour, so we need to check 30 minutes before
        # or after to check if these tables are available.
        bookingDateStart = booking.booked_at - timedelta(minutes = 30)
        bookingDateEnd = booking.booked_at + timedelta(minutes = 30)
        bookings = Booking.query.filter(Booking.booked_at >= bookingDateStart.strftime(dateFormat),
                                        Booking.booked_at <= bookingDateEnd.strftime(dateFormat)
                                        ).all()

        # Get free tables
        tables = Table.query.order_by(Table.seats).all()
        for booking in bookings:
            ocupied_tables = booking.tables
            for ocupied_table in ocupied_tables:
                tables.remove(ocupied_table)

        return tables
