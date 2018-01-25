import click
from models import db, UserRole, User, Table, Booking
from flask import Flask
from datetime import datetime

@click.group()
def cli():
    click.echo("Wellcome.")

@cli.command()
def init_database():
    print "Creating database with demo data..."

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
    db.init_app(app)

    # remove file if exists
    import os.path
    import sys
    file = "./restaurant.db"
    database_exists = os.path.isfile(file)
    if database_exists:
        os.remove(file)

    with app.app_context():
        db.create_all()
    print "Database models created."

    admin = UserRole(name='Admin', desc='App admin')
    manager = UserRole(name='Manager', desc='Restaurant manager')
    employee = UserRole(name='Employee', desc='Restaurant employee')
    customer = UserRole(name='Customer', desc='Restaurant customer')
    with app.app_context():
        db.session.add(admin)
        db.session.add(manager)
        db.session.add(employee)
        db.session.add(customer)

    josu = User(name='Josu', password='josupass', role=admin)
    maria = User(name='Maria', password='mariapass', role=customer)
    with app.app_context():
        db.session.add(josu)
        db.session.add(maria)

    table1 = Table(desc='Table closest to front door', seats=4)
    table2 = Table(desc='Table number 2', seats=2)
    table3 = Table(desc='Circular table', seats=8)
    table4 = Table(desc='Table number 4', seats=2)
    table5 = Table(desc='Table number 5', seats=2)
    table6 = Table(desc='Table number 6', seats=4)
    table7 = Table(desc='Table number 7', seats=4)
    table8 = Table(desc='Table number 8', seats=4)
    table9 = Table(desc='Table number 9', seats=4)
    table10 = Table(desc='Table number 10', seats=6)
    with app.app_context():
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
        db.session.commit()

    booking = Booking(creator=josu, persons=5, booked_at=datetime.strptime("2018-01-01 14:00", "%Y-%m-%d %H:%M") )
    booking.tables.append(table1)
    booking.tables.append(table2)
    with app.app_context():
        db.session.add(booking)

        db.session.commit()
    print "Init data created in database"

if __name__ == '__main__':
    cli()
