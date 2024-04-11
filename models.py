from creation import db
from enums import user_type, status, month, Cms_Enum, bill_type
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.Enum(user_type), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_validated = db.Column(db.Boolean, default=False)

    unit = db.relationship("Unit", backref="users")
    cms = db.relationship("Cms", backref="users")

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

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lease_agreement_id = db.Column(db.Integer, db.ForeignKey('lease_agreements.lease_agreement_id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    image_path = db.Column(db.String(255), nullable=True) 
    status = db.Column(db.Enum(status), default=status.PENDING)
    
    lease = db.relationship("LeaseAgreement", backref="payments")

class Bill(db.Model):
    __tablename__ = 'bills'

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    month = db.Column(db.Enum(month), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    breakdown = db.Column(db.Text, nullable=True)
    bill_type = db.Column(db.Enum(bill_type), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Enum(status), default=status.PENDING)

    unit = db.relationship("Unit", backref="bills")

class Cms(db.Model):
    __tablename__ = 'cms'
    
    cms_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cms_type = db.Column(db.Enum(Cms_Enum), nullable=False)
    date_posted = db.Column(db.Date, nullable=False)
    time_posted = db.Column(db.Time, nullable=False)
    date_to_post = db.Column(db.Date, nullable=True)
    date_to_end = db.Column(db.Date, nullable=True)
    archive = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(status), default=status.PENDING)

class AccessControl(db.Model):
    __tablename__ = 'access_control'

    module_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_name = db.Column(db.String(200))
    super_admin = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    owner = db.Column(db.Boolean)
    tenant = db.Column(db.Boolean)
    guest = db.Column(db.Boolean)
