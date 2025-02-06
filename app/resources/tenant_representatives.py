from .common import Resource, request, IntegrityError
from ..models import TenantRepresentatives
from ..extensions import db

class TenantRepresentativesResource(Resource):
    def get(self, tenant_id=None):
        if tenant_id:
            tenant_representatives = TenantRepresentatives.query.filter(TenantRepresentatives.tenant_id == tenant_id).all()
            if tenant_representatives:
                return [{
                    'tenant_id': tenant_representative.tenant_id,
                    'first_name': tenant_representative.first_name,
                    'last_name': tenant_representative.last_name,
                    'image': tenant_representative.image
                }for tenant_representative in tenant_representatives]
            else:
                return {'message': 'Tenant representative not found'}, 200
        else:
            tenant_representatives = TenantRepresentatives.query.all()
            return [{
                'tenant_id': tenant_representative.tenant_id,
                'first_name': tenant_representative.first_name,
                'last_name': tenant_representative.last_name,
                'image': tenant_representative.image
            }for tenant_representative in tenant_representatives]

    def post(self):
        try:
            data = request.get_json()

            new_tenant_representative = TenantRepresentatives(**data)
            db.session.add(new_tenant_representative)
            db.session.commit()

            response_data = {
                'message': 'Tenant representative created successfully',
                'tenant_representative_id': new_tenant_representative.tenant_id,
            }

            return response_data, 201
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error creating tenant representative'}, 500