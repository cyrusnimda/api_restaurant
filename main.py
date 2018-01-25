from flask import Flask, jsonify
from models import db, UserRole, User, Table, Booking

app = Flask(__name__)

# Load config file
app.config.from_pyfile('config.cfg')
print "Config file loaded."

# Load database model
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    users = User.query.all()
    usersJSON = []
    for user in users:
        usersJSON.append(user.json())
    return jsonify({'users': usersJSON})


if __name__ == '__main__':
    app.run()
