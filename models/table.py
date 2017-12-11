class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200))
    seats = db.Column(db.Integer)
