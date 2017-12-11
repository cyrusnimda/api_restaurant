class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(200))
    users = db.relationship('Booking', backref='role', lazy=True)
