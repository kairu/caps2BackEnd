from .common import Resource, request, IntegrityError, datetime
from ..models import FeedbackComplaintNotes
from ..extensions import db

class FeedbackComplaintNotesResource(Resource):
    
    def get(self, cms_id=None):
        if cms_id:
            feedback_complaint_notes = FeedbackComplaintNotes.query.filter_by(cms_id=cms_id).all()
            if feedback_complaint_notes:
                return [{'fc_id': note.fc_id, 'cms_id': note.cms_id, 'notes': note.notes} for note in feedback_complaint_notes]
            return {'message': 'No notes found for this cms_id'}, 404
        else:
            feedback_complaint_notes = FeedbackComplaintNotes.query.all()
            return [{'fc_id': note.fc_id, 'cms_id': note.cms_id, 'notes': note.notes} for note in feedback_complaint_notes]
    
    # Add data
    def post(self):
        try:
            data = request.get_json()
            
            new_feedback_complaint_notes = FeedbackComplaintNotes(**data)
            db.session.add(new_feedback_complaint_notes)
            db.session.commit()
            return {'message': 'Feedback/Complaint/Notes added successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f'Error creating feedback/complaint/notes: {str(e)}')
            return {'error': 'Error creating feedback/complaint/notes'}, 500
        
    # Edit Data
    # For editting cms_id will be fc_id
    def put(self, cms_id):
        data = request.get_json()
        feedback_complaint_notes = FeedbackComplaintNotes.query.get(cms_id)
        if feedback_complaint_notes:
            feedback_complaint_notes.cms_id = data['cms_id']
            feedback_complaint_notes.notes = data['notes']

            db.session.commit()
            return {'message': 'Feedback/Complaint/Notes updated Successfully'}
        else:
            return {'message': 'Feedback/Complaint/Notes not found'}
        
    # Delete notes Data
    # For deleting cms_id will be fc_id
    def delete(self, cmd_id):
        feedback_complaint_notes = FeedbackComplaintNotes.query.get(cmd_id)
        if feedback_complaint_notes:
            db.session.delete(feedback_complaint_notes)
            db.session.commit()
            return {'message': 'Feedback/Complaint/Notes deleted Successfully'}
        else:
            return {'message': 'Feedback/Complaint/Notes not found'}