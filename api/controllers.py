from datetime import timedelta
from .models import Table, Booking, db

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
        persons = int(booking.persons)
        best_tables, persons_left = self._get_best_table(tables, persons, [])

        return (None if persons_left > 0 else best_tables)

    def get_bookings_from_date(self, bookingDate):
        hour = bookingDate.strftime("%H:%M")
        if hour == "00:00":
            # It is a whole day date.
            bookingDateStart = bookingDate.replace(hour=9, minute=00)
            bookingDateEnd = bookingDate.replace(hour=23, minute=00)
        else:
            # Booking are for 1 hour, so we need to check 30 minutes before
            # or after to check if these tables are available.
            bookingDateStart = bookingDate - timedelta(minutes = 30)
            bookingDateEnd = bookingDate + timedelta(minutes = 30)
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

    def save_booking(self, booking):
        # Get free tables
        free_tables = self.get_free_tables(booking)

        # Get bets tables for this booking.
        best_tables = self.get_best_tables_for_a_booking(free_tables, booking)
        if None == best_tables:
            raise Exception("There are not that many tables availables")

        for table in best_tables:
            booking.tables.append(table)
        db.session.add(booking)
        db.session.commit()
