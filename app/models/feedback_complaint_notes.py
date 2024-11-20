from ..extensions import db
from ..enums.status import status
from ..enums.cmsEnum import Cms_Enum

class FeedbackComplaintNotes(db.Model):
    __tablename__ = 'feedback_complaint_notes'
    
    fc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cms_id = db.Column(db.Integer, db.ForeignKey('cms.cms_id'), nullable=False)
    notes = db.Column(db.Text, nullable=False)