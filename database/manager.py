from datetime import datetime

"""
    Database controller class.
"""
class DatabaseManager():
    def __init__(self, db):
        self.db = db

    #Create database and insert some init data.
    def initDataBase(self):
        self.db.create_all()
        print "Database models created."

        admin = UserRole(name='Admin', desc='App admin')
        manager = UserRole(name='Manager', desc='Restaurant manager')
        employee = UserRole(name='Employee', desc='Restaurant employee')
        customer = UserRole(name='Customer', desc='Restaurant customer')
        self.db.session.add(admin)
        self.db.session.add(manager)
        self.db.session.add(employee)
        self.db.session.add(customer)

        josu = User(name='Josu', password='josupass', role=admin)
        maria = User(name='Maria', password='mariapass', role=customer)
        self.db.session.add(josu)
        self.db.session.add(maria)

        table1 = Table(desc='Table closest to front door', seats=4)
        table2 = Table(seats=2)
        table3 = Table(desc='Circular table', seats=8)
        self.db.session.add(table1)
        self.db.session.add(table2)
        self.db.session.add(table3)

        booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
        booking.tables.append(table1)
        booking.tables.append(table2)

        self.db.session.add(booking)

        self.db.session.commit()
        print "Init data created in database"
