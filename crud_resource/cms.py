from creation import db, Cms
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class CmsResource(Resource):
    def get(self, cms_id=None):
        if cms_id:
            cms = Cms.query.get(cms_id)
            if cms:
                return{
                    'cms_id': cms.cms_id,
                    'user_id': cms.user_id,
                    'title': cms.title,
                    'description': cms.description,
                    'cms_type': cms.cms_type.name,
                    'date_posted': cms.date_posted.isoformat() if cms.date_posted else None,
                    'time_posted': cms.time_posted.isoformat() if cms.time_posted else None
                }
            else:
                return {'message': 'No such Content'},404
        else:
            cmss = Cms.query.all()
            return [{
                'cms_id': cms.cms_id,
                'user_id': cms.user_id,
                'title': cms.title,
                'description': cms.description,
                'cms_type': cms.cms_type.name,
                'date_posted': cms.date_posted.isoformat() if cms.date_posted else None,
                'time_posted': cms.time_posted.isoformat() if cms.time_posted else None
            }for cms in cmss]
        
    # Add data
    def post(self):
        try:
            data = request.get_json()

            # Check if cms exists.
            existing_cms = Cms.query.filtery_by(cms_id=data['cms_id']).first()
            if existing_cms:
                return {'error': 'Content already exists'}, 409
            
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
            cms.user_id = data['user_id']
            cms.title = data['title']
            cms.description = data['description']
            cms.cms_type = data['cms_type']
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
            return {'message': 'Deleted Content Data suiccessfully'}
        else:
            return {'message': 'Content Data not found'}, 404