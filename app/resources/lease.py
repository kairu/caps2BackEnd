from .common import Resource, request, IntegrityError
from ..models import LeaseAgreement
from ..extensions import db

class LeaseAgreementResource(Resource):
    def get(self, lease_id_or_tenant_id=None):
        if lease_id_or_tenant_id:
            if lease_id_or_tenant_id.isdigit():
                leases = LeaseAgreement.query.get(lease_id_or_tenant_id)
            elif 'OWNER' in lease_id_or_tenant_id:
                lease_id_or_tenant_id = int(lease_id_or_tenant_id.replace('OWNER', '').strip())
                leases = LeaseAgreement.query.filter_by(owner_id = lease_id_or_tenant_id).all()
            else:
                lease_id_or_tenant_id = int(lease_id_or_tenant_id.replace('TENANT', '').strip())
                leases = LeaseAgreement.query.filter_by(tenant_id=lease_id_or_tenant_id).all()
            if leases:
                return[{
                    'lease_agreement_id': lease.lease_agreement_id,
                    'unit_id': lease.unit_id,
                    'owner_id': lease.owner_id,
                    'tenant_id': lease.tenant_id,
                    'contract': lease.contract,
                    'start_date': lease.start_date.isoformat() if lease.start_date else None,
                    'end_date': lease.end_date.isoformat() if lease.end_date else None,
                    'monthly_rent': lease.monthly_rent,
                    'security_deposit': lease.security_deposit,
                    'remaining_balance': lease.remaining_balance
                }for lease in leases]
            else:
                return {'message': 'Lease not found'}, 404
        else:
            leases = LeaseAgreement.query.all()
            return [{
                'lease_agreement_id': lease.lease_agreement_id,
                'unit_id': lease.unit_id,
                'owner_id': lease.owner_id,
                'tenant_id': lease.tenant_id,
                'contract': lease.contract,
                'start_date': lease.start_date.isoformat() if lease.start_date else None,
                'end_date': lease.end_date.isoformat() if lease.end_date else None,
                'monthly_rent': lease.monthly_rent,
                'security_deposit': lease.security_deposit,
                'remaining_balance': lease.remaining_balance
                    
            }for lease in leases]
    
    # Add data
    def post(self):
        try:
            data = request.get_json()

            # Check if lease exists
            # existing_lease = LeaseAgreement.query.filter_by(lease_agreement_id=data['lease_agreement_id'])
            # if existing_lease:
            #     return {'error': 'This lease already exists'},409
            
            new_lease = LeaseAgreement(**data)
            db.session.add(new_lease)
            db.session.commit()
            
            response_data = {
                'message': 'Lease created successfully',
                'lease_agreement_id': new_lease.lease_agreement_id,
            }
            return response_data, 201
        except IntegrityError as e:
            db.session.rollback()
            return{'error': 'Error creating lease'}, 500
        
    # Edit Data
    def put(self, lease_id_or_tenant_id):
        lease = LeaseAgreement.query.get(lease_id_or_tenant_id)
        if lease:
            data = request.get_json()
            if 'unit_id' in data:
                lease.unit_id = data['unit_id']
            if 'owner_id' in data:
                lease.owner_id = data['owner_id']
            if 'tenant_id' in data:
                lease.tenant_id = data['tenant_id']
            if 'contract' in data:
                lease.contract = data['contract']
            if 'start_date' in data:
                lease.start_date = data['start_date']
            if 'end_date' in data:
                lease.end_date = data['end_date']
            if 'monthly_rent' in data:
                lease.monthly_rent = data['monthly_rent']
            if 'security_deposit' in data:
                lease.security_deposit = data['security_deposit']
            if 'remaining_balance' in data:
                lease.remaining_balance = data['remaining_balance']
            if 'deduct_balance' in data:
                lease.remaining_balance -= data['deduct_balance']
            if 'add_balance' in data:
                lease.remaining_balance += data['add_balance']
            db.session.commit()
            return{ 'message': 'Lease Agreement updated successfully'}
        else:
            return {'message': 'Lease Agreement not found'}, 404
        
    # Prohibit deletion of lease agreement
    def delete(self, lease_agreement_id):
        return {'message': 'Cannot delete lease agreements!'}, 404