from ..extensions import db
from ..enums.userType import user_type

class TenantRepresentatives(db.Model):
    __tablename__ = 'tenant_representatives'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image =  db.Column(db.String(255), nullable=False)