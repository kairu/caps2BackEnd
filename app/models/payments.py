from ..extensions import db
from ..enums.status import status

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lease_agreement_id = db.Column(db.Integer, db.ForeignKey('lease_agreements.lease_agreement_id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    image_path = db.Column(db.String(255), nullable=True) 
    status = db.Column(db.Enum(status), default=status.PENDING)
    
    lease = db.relationship("LeaseAgreement", backref="payments")