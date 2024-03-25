from creation import db, AccessControl
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class AccessControlResource(Resource):
    def get(self):
        controls = AccessControl.query.all()
        return [{
            'module_name': control.module_name,
            'super_admin': control.super_admin,
            'admin': control.admin,
            'owner': control.owner,
            'tenant': control.tenant,
            'guest': control.guest
        } for control in controls]

        # json_data = json.dumps(data)
        # return json_data
    
    # Edit/update data
    def put(self):
        data = request.get_json()
        module = AccessControl.query.filter_by(module_name=data['module_name']).first()
        print(data)
        if module:
            module.module_name = data['module_name']
            module.super_admin = data['super_admin']
            module.admin = data['admin']
            module.owner = data['owner']
            module.tenant = data['tenant']
            module.guest = data['guest']
            db.session.commit()
            return {'message': 'Access updated successfully'}
        else:
            return {'message': 'Access not found'}, 404