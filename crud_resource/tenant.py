from creation import db, Tenant
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class TenantResource(Resource):
    def get(self, tenant_id=None):
        if tenant_id:
            tenant = Tenant.query.get(tenant_id)
            if tenant:
                return{
                    'tenant_id': tenant.tenant_id,
                    'user_id': tenant.user_id,
                    'move_in_date': tenant.move_in_date.isoformat() if tenant.move_in_date else None,
                    'move_out_date': tenant.move_out_date.isoformat() if tenant.move_out_date else None
                }
            else:
                return {'message': 'Tenant not found'}, 404
        else:
            tenants = Tenant.query.all()
            return [{
                'tenant_id': tenant.tenant_id,
                'user_id': tenant.user_id,
                'move_in_date': tenant.move_in_date.isoformat() if tenant.move_in_date else None,
                'move_out_date': tenant.move_out_date.isoformat() if tenant.move_out_date else None
            } for tenant in tenants]
    
    # Add data
    def post(self):
        try:
            data = request.get_json()

            # Check if tenant already exists
            exisiting_tenant = Tenant.query.filter_by(user_id=data['user_id']).first()
            if exisiting_tenant:
                return {'error': 'Tenant already exsists'}, 409
            
            new_tenant = Tenant(**data)
            db.session.add(new_tenant)
            db.session.commit()
            return {'message': 'Tenant created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error creating tenant: {str(e)}")
            return {'error': 'Error creating tenant'}, 500
        
    # Edit data
    def put(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            data = request.get_json()

            tenant.move_in_date = data['move_in_date']
            tenant.move_out_date = data['move_out_date']
            return {'message': 'Tenant updated successfully'}
        else:
            return {'message': 'Tenant not found'}, 404
        
    def delete(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return {'message': 'Tenant deleted successfully'}
        else:
            return {'message': 'Tenant not found'}, 404