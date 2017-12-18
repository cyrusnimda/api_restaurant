class Booking():
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    tables = db.relationship('Table', secondary=booking_tables, lazy='subquery')
    persons = db.Column(db.Integer)
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime)
