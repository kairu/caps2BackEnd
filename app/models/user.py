from ..extensions import db
from ..enums.userType import user_type

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