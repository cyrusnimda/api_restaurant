import click

@click.command()
@click.option('--init-database', default=None, help='Create database with demo data.')

def cli(init_database):
    if initDatabase:
        #Load init data in database
        # remove file if exists
        import os.path
        import sys
        file = "./restaurant.db"
        database_exists = os.path.isfile(file)
        if database_exists:
            os.remove(file)

        db.create_all()
        print "Database models created."

        admin = UserRole(name='Admin', desc='App admin')
        manager = UserRole(name='Manager', desc='Restaurant manager')
        employee = UserRole(name='Employee', desc='Restaurant employee')
        customer = UserRole(name='Customer', desc='Restaurant customer')
        db.session.add(admin)
        db.session.add(manager)
        db.session.add(employee)
        db.session.add(customer)

        josu = User(name='Josu', password='josupass', role=admin)
        maria = User(name='Maria', password='mariapass', role=customer)
        db.session.add(josu)
        db.session.add(maria)

        table1 = Table(desc='Table closest to front door', seats=4)
        table2 = Table(seats=2)
        table3 = Table(desc='Circular table', seats=8)
        table4 = Table(seats=2)
        table5 = Table(seats=2)
        table6 = Table(seats=4)
        table7 = Table(seats=4)
        table8 = Table(seats=4)
        table9 = Table(seats=4)
        table10 = Table(seats=6)
        db.session.add(table1)
        db.session.add(table2)
        db.session.add(table3)
        db.session.add(table4)
        db.session.add(table5)
        db.session.add(table6)
        db.session.add(table7)
        db.session.add(table8)
        db.session.add(table9)
        db.session.add(table10)

        booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
        booking.tables.append(table1)
        booking.tables.append(table2)
        db.session.add(booking)

        db.session.commit()
        print "Init data created in database"
