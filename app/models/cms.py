from ..extensions import db
from ..enums.status import status
from ..enums.cmsEnum import Cms_Enum

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
    # 1 = Admin/Super_admin
    # Whole Number #### = Owner, 
    # -2 = Tenant(Might not use), 
    # Negative Number -#### = Both
    notify_to = db.Column(db.Integer, nullable=True)

    notes = db.relationship("FeedbackComplaintNotes", backref="cms")