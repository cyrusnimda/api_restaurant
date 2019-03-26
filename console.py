import click
from api.models import db, UserRole, User, Table, Booking
from api.main import app
from datetime import datetime
import bcrypt
import unittest

@click.group()
def cli():
    pass

@cli.command()
def run_api():
    app.run(port=app.config["PORT"])

@cli.command()
def run_tests():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@cli.command()
def init_database():
    print ("Creating database...")
    db.init_app(app)

    with app.app_context():
        db.create_all()
    print ("Database models created.")

if __name__ == '__main__':
    cli()
