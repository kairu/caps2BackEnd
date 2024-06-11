from ..extensions import db
from ..enums.month import month
from ..enums.billType import bill_type
from ..enums.status import status

class Bill(db.Model):
    __tablename__ = 'bills'

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    month = db.Column(db.Enum(month), nullable=True)
    soa_id = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    delinquent_amount = db.Column(db.Float, nullable=True)
    breakdown = db.Column(db.Text, nullable=True)
    bill_type = db.Column(db.Enum(bill_type), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    image_path = db.Column(db.String(255), nullable=True) 
    status = db.Column(db.Enum(status), default=status.PENDING)

    unit = db.relationship("Unit", backref="bills")
    