import click

@click.command()
@click.option('--init-database', default=None, help='Create database with demo data.')

def cli(init_database):
    if initDatabase:
        #Load init data in database
        if app.config["ADD_INITIAL_DATA"] == True:
            # remove file if exists
            import os.path
            import sys
            file = "./database/restaurant.db"
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
            db.session.add(table1)
            db.session.add(table2)
            db.session.add(table3)

            booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
            booking.tables.append(table1)
            booking.tables.append(table2)
            db.session.add(booking)

            db.session.commit()
            print "Init data created in database"
