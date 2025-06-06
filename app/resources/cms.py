from .common import Resource, request, IntegrityError, datetime
from ..models import Cms
from ..extensions import db

class CmsResource(Resource):
    def get(self, cms_id=None):
        if cms_id:
            cms = Cms.query.get(cms_id)
            if cms:
                cms_data = {
                    'cms_id': cms.cms_id,
                    'user_id': cms.user_id,
                    'image_path': cms.image_path,
                    'title': cms.title,
                    'description': cms.description,
                    'cms_type': cms.cms_type.name,
                    'date_posted': cms.date_posted.isoformat() if cms.date_posted else None,
                    'time_posted': cms.time_posted.isoformat() if cms.time_posted else None,
                    'date_to_post': cms.date_to_post.isoformat() if cms.date_to_post else None,
                    'date_to_end': cms.date_to_end.isoformat() if cms.date_to_end else None,
                    'archive': cms.archive,
                    'status': cms.status.name,
                    'notify_to': cms.notify_to
                }
                
                cms_data['notes'] = []
                
                for notes in cms.notes:
                    note_data ={
                        'fc_id': notes.fc_id,
                        'cms_id': notes.cms_id,
                        'notes': notes.notes
                    }
                    
                cms_data['notes'].append(note_data)
                
                return cms_data
            else:
                return {'message': 'No such Content'},404
        else:
            cmss = Cms.query.all()
            cmss_data = []
            
            for cms in cmss:
                cms_data = {
                'cms_id': cms.cms_id,
                'user_id': cms.user_id,
                'image_path': cms.image_path,
                'title': cms.title,
                'description': cms.description,
                'cms_type': cms.cms_type.name,
                'date_posted': cms.date_posted.isoformat() if cms.date_posted else None,
                'time_posted': cms.time_posted.isoformat() if cms.time_posted else None,
                'date_to_post': cms.date_to_post.isoformat() if cms.date_to_post else None,
                'date_to_end': cms.date_to_end.isoformat() if cms.date_to_end else None,
                'archive': cms.archive,
                'status': cms.status.name,
                'notify_to': cms.notify_to
                }
                
                cms_data['notes'] = []
                
                if cms.notes:
                    for notes in cms.notes:
                        note_data ={
                            'fc_id': notes.fc_id,
                            'cms_id': notes.cms_id,
                            'notes': notes.notes
                        }
                        cms_data['notes'].append(note_data)
                
                cmss_data.append(cms_data)                
            return cmss_data
        
    # Add data
    def post(self):
        try:
            data = request.get_json()

            data['date_posted'] = datetime.now().date()
            data['time_posted'] = datetime.now().time()
            
            new_cms = Cms(**data)
            db.session.add(new_cms)
            db.session.commit()
            return {'message': 'Content created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f'Error creating content: {str(e)}')
            return {'error': 'Error creating content'}, 500
        
    # Edit Data
    def put(self, cms_id):
        data = request.get_json()
        cms = Cms.query.get(cms_id)
        if cms:
            if 'user_id' in data:
                cms.user_id = data['user_id']
            if 'image_path' in data:
                cms.image_path = data['image_path']
            if 'title' in data:
                cms.title = data['title']
            if 'description' in data:
                cms.description = data['description']
            if 'cms_type' in data:
                cms.cms_type = data['cms_type']
            if 'date_posted' in data:
                cms.date_posted = data['date_posted']
            if 'time_posted' in data:
                cms.time_posted = data['time_posted']
            if 'date_to_post' in data:
                cms.date_to_post = data['date_to_post']
            if 'date_to_end' in data:
                cms.date_to_end = data['date_to_end']
            if 'archive' in data:
                cms.archive = data['archive']
            if 'status' in data:
                cms.status = data['status']
            if 'notify_to' in data:
                cms.notify_to = data['notify_to']
                
            if 'feedback' not in data:
                cms.date_posted = datetime.now().date()
                cms.time_posted = datetime.now().time()

            db.session.commit()
            return {'message': 'Content updated Successfully',
                    'date_posted': cms.date_posted.isoformat(),
                    'time_posted': cms.time_posted.isoformat()
                    }
        else:
            return {'message': 'Content not found'}

    # Delete CMS Data
    def delete(self, cms_id):
        cms = Cms.query.get(cms_id)
        if cms:
            db.session.delete(cms)
            db.session.commit()
            return {'message': 'Deleted Content Data successfully'}
        else:
            return {'message': 'Content Data not found'}, 404
        
    