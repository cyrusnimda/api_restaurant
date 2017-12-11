class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    token = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    bookings = db.relationship('Booking', backref='creator', lazy=True)
