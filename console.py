import click
from api.main import create_app
from api.models import db
import unittest
from api.repository import db_feeds

app = create_app()

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
    #db.init_app(app)

    with app.app_context():
        db.create_all()
    print ("Database models created.")


@cli.command()
def feed_database():
    print("Feeding database with initial data...")
    with app.app_context():
        db_feeds(db)
    print("Database fed with initial data.")

if __name__ == '__main__':
    cli()
