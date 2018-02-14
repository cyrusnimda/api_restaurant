from datetime import datetime, timedelta
from models import Table, Booking

class BookingController():
    DATE_FORMAT = "%Y-%m-%d %H:%M"

    def _get_best_table(self, tables, persons, assigned_tables):
        while persons > 0 and len(tables) > 0:
            for index, table in enumerate(tables):
                if persons <= table.seats or len(tables) -1 == index:
                    tables.remove(table)
                    persons = int(persons) - table.seats
                    assigned_tables.append(table)
                    break
        return [assigned_tables, persons]

    """
        From a list of tables, and a number of persons, we get the best tables,
        That means we get the biggest table we can that fits the people.

        @parameter tables, the list of tables availables
        @parameter booking, the booking object with the people, date, etc.
        @return None if there are not that many tables availables
        @return List best_tables.
    """
    def get_best_tables_for_a_booking(self, tables, booking):
        persons = booking.persons
        best_tables, persons_left = self._get_best_table(tables, persons, [])

        return (None if persons_left > 0 else best_tables)

    def get_bookings_from_date(self, bookingDate):
        # Booking are for 1 hour, so we need to check 30 minutes before
        # or after to check if these tables are available.
        bookingDateStart = bookingDate - timedelta(minutes = 30)
        bookingDateEnd = bookingDate + timedelta(minutes = 30)
        bookings = Booking.query.filter(Booking.booked_at >= bookingDateStart.strftime(self.DATE_FORMAT),
                                        Booking.booked_at <= bookingDateEnd.strftime(self.DATE_FORMAT)
                                        ).all()
        return bookings

    def get_bookings_today(self):
        bookingDateStart = datetime.now()
        bookingDateStart = bookingDateStart.replace(hour=9, minute=00)

        bookingDateEnd = datetime.now()
        bookingDateEnd = bookingDateEnd.replace(hour=23, minute=00)
        bookings = Booking.query.filter(Booking.booked_at >= bookingDateStart.strftime(self.DATE_FORMAT),
                                        Booking.booked_at <= bookingDateEnd.strftime(self.DATE_FORMAT)
                                        ).all()
        return bookings

    def get_free_tables(self, booking):
        bookings = self.get_bookings_from_date(booking.booked_at)

        # Get free tables
        tables = Table.query.order_by(Table.seats).all()
        for booking in bookings:
            ocupied_tables = booking.tables
            for ocupied_table in ocupied_tables:
                tables.remove(ocupied_table)

        return tables

    def get_booked_tables(self, bookings):
        bookedTables = 0
        for booking in bookings:
            bookedTables = bookedTables + len(booking.tables)
        return bookedTables

    def get_bookings_from_exact_date(self, bookingDate):
        return Booking.query.filter(Booking.booked_at.startswith( bookingDate.strftime(self.DATE_FORMAT) )).all()
