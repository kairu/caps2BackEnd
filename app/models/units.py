from ..extensions import db

class Unit(db.Model):
    __tablename__ = 'units'

    unit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    tower_number = db.Column(db.Integer, nullable=False)
    floor_number = db.Column(db.Integer, nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    sq_foot = db.Column(db.Integer, nullable=True)
    number_of_bedrooms = db.Column(db.Integer, nullable=True)
    number_of_bathrooms = db.Column(db.Integer, nullable=True)
    parking_slot = db.Column(db.String(20), nullable=True)
    remaining_balance = db.Column(db.Integer, nullable=True)