from ..extensions import db

class AccessControl(db.Model):
    __tablename__ = 'access_control'

    module_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_name = db.Column(db.String(200))
    super_admin = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    owner = db.Column(db.Boolean)
    tenant = db.Column(db.Boolean)
    guest = db.Column(db.Boolean)