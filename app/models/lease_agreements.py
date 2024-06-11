from ..extensions import db

class LeaseAgreement(db.Model):
    __tablename__ = 'lease_agreements'

    lease_agreement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    contract = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    monthly_rent = db.Column(db.Integer, nullable=False)
    security_deposit = db.Column(db.Integer, nullable=True)
    remaining_balance = db.Column(db.Integer, nullable=True)

    unit = db.relationship("Unit", backref="lease_agreements")
    owner = db.relationship("User", foreign_keys=[owner_id], backref="lease_agreements")
