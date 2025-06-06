from .common import re, Resource, request, IntegrityError
from ..models import User
from ..extensions import db

class UserResource(Resource):
    
    def get_tenant_info(self, tenant_id):
        tenant_user = User.query.get(tenant_id)
        if tenant_user:
            return {
                'user_id': tenant_user.user_id,
                'first_name': tenant_user.first_name,
                'last_name': tenant_user.last_name,
                'email': tenant_user.email,
                'mobile_number': tenant_user.mobile_number,
                'user_type': tenant_user.user_type.name,
                'is_validated': tenant_user.is_validated,
                'lessor_id': tenant_user.lessor_id
            }
        return None
        
    # Get Data
    def get(self, email_or_user_id=None):
        if email_or_user_id:
            if re.match(r'^[\w\.-]+@[\w\.-]+$', email_or_user_id):
                user = User.query.filter(User.email == email_or_user_id).first()
            else:
                user = User.query.get(email_or_user_id)
                
            if user:
                user_data = {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'mobile_number': user.mobile_number,
                    'user_type': user.user_type.name,
                    'is_active': user.is_active,
                    'is_validated': user.is_validated,
                    'lessor_id': user.lessor_id
                }

                # Adding relationships data
                user_data['units'] = []

                for unit in user.unit:
                    unit_data = {
                        'unit_id': unit.unit_id,
                        'tower_number': unit.tower_number,
                        'floor_number': unit.floor_number,
                        'unit_number': unit.unit_number,
                        'unit_type': unit.unit_type,
                        'sq_foot': unit.sq_foot,
                        'number_of_bedrooms': unit.number_of_bedrooms,
                        'number_of_bathrooms': unit.number_of_bathrooms,
                        'parking_slot': unit.parking_slot,
                        'remaining_balance': unit.remaining_balance,
                        'bills': []  # Initialize bills list for each unit
                    }

                    # Add bills to the unit
                    for bill in unit.bills:
                        unit_data['bills'].append({
                            'bill_id': bill.bill_id,
                            'unit_id': bill.unit_id,
                            'month': bill.month.name if bill.month else None,
                            'soa_id': bill.soa_id,
                            'due_date': bill.due_date.isoformat() if bill.due_date else None,
                            'total_amount': bill.total_amount,
                            'delinquent_amount': bill.delinquent_amount,
                            'breakdown': bill.breakdown,
                            'bill_type': bill.bill_type.name,
                            'payment_method': bill.payment_method,
                            'image_path': bill.image_path,
                            'status': bill.status.name
                        })
                    
                    user_data['units'].append(unit_data)


                if user.lease_agreements:
                    user_data['lease_agreements'] = [{
                        'lease_agreement_id': agreement.lease_agreement_id,
                        'unit_id': agreement.unit_id,
                        'tenant_id': agreement.tenant_id,
                        'contract': agreement.contract,
                        'start_date': agreement.start_date.isoformat() if agreement.start_date else None,
                        'end_date': agreement.end_date.isoformat() if agreement.end_date else None,
                        'monthly_rent': agreement.monthly_rent,
                        'security_deposit': agreement.security_deposit,
                        'remaining_balance': agreement.remaining_balance,
                        'tenant_info': self.get_tenant_info(agreement.tenant_id),
                        'payments': [{
                            'payment_id': payment.payment_id,
                            'lease_agreement_id': agreement.lease_agreement_id,
                            'due_date': payment.due_date.isoformat() if payment.due_date else None,
                            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                            'amount': payment.amount,
                            'payment_method': payment.payment_method,
                            'reference_number': payment.reference_number,
                            'image_path': payment.image_path,
                            'status': payment.status.name
                        } for payment in agreement.payments]
                    } for agreement in user.lease_agreements]

                if user.cms:
                    user_data['cms'] = [{
                        'cms_id': cms.cms_id,
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
                        'notify_to': cms.notify_to,
                        'notes': [{
                            'fc_id': note.fc_id,
                            'cms_id': note.cms_id,
                            'notes': note.notes
                        } for note in cms.notes]
                    } for cms in user.cms]

                return user_data
            else:
                return {'message': 'User not found'}
        else:
            users = User.query.all()
            users_data = []
            for user in users:
                user_data = {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'mobile_number': user.mobile_number,
                    'user_type': user.user_type.name,
                    'is_active': user.is_active,
                    'is_validated': user.is_validated,
                    'lessor_id': user.lessor_id
                }

                # Adding relationships data
                user_data['units'] = []

                for unit in user.unit:
                    unit_data = {
                        'unit_id': unit.unit_id,
                        'tower_number': unit.tower_number,
                        'floor_number': unit.floor_number,
                        'unit_number': unit.unit_number,
                        'sq_foot': unit.sq_foot,
                        'unit_type': unit.unit_type,
                        'number_of_bedrooms': unit.number_of_bedrooms,
                        'number_of_bathrooms': unit.number_of_bathrooms,
                        'parking_slot': unit.parking_slot,
                        'remaining_balance': unit.remaining_balance,
                        'bills': []  # Initialize bills list for each unit
                    }

                    # Add bills to the unit
                    for bill in unit.bills:
                        unit_data['bills'].append({
                            'bill_id': bill.bill_id,
                            'unit_id': bill.unit_id,
                            'month': bill.month.name if bill.month else None,
                            'soa_id': bill.soa_id,
                            'due_date': bill.due_date.isoformat() if bill.due_date else None,
                            'total_amount': bill.total_amount,
                            'delinquent_amount': bill.delinquent_amount,
                            'breakdown': bill.breakdown,
                            'bill_type': bill.bill_type.name,
                            'payment_method': bill.payment_method,
                            'image_path': bill.image_path,
                            'status': bill.status.name
                        })
                    
                    user_data['units'].append(unit_data)

                if user.lease_agreements:
                    user_data['lease_agreements'] = [{
                        'lease_agreement_id': agreement.lease_agreement_id,
                        'unit_id': agreement.unit_id,
                        'contract': agreement.contract,
                        'start_date': agreement.start_date.isoformat() if agreement.start_date else None,
                        'end_date': agreement.end_date.isoformat() if agreement.end_date else None,
                        'monthly_rent': agreement.monthly_rent,
                        'security_deposit': agreement.security_deposit,
                        'remaining_balance': agreement.remaining_balance,
                        'tenant_info': self.get_tenant_info(agreement.tenant_id),
                        'payments': [{
                            'payment_id': payment.payment_id,
                            'due_date': payment.due_date.isoformat() if payment.due_date else None,
                            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                            'amount': payment.amount,
                            'payment_method': payment.payment_method,
                            'reference_number': payment.reference_number,
                            'image_path': payment.image_path,
                            'status': payment.status.name
                        } for payment in agreement.payments]
                    } for agreement in user.lease_agreements]

                if user.cms:
                    user_data['cms'] = [{
                        'cms_id': cms.cms_id,
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
                        'notify_to': cms.notify_to,
                        'notes': [{
                            'fc_id': note.fc_id,
                            'cms_id': note.cms_id,
                            'notes': note.notes
                        } for note in cms.notes]
                    } for cms in user.cms]
                   
                users_data.append(user_data)
                
            return users_data
            
    # Adding data
    def post(self):
        try:
            data = request.get_json()

            # Check if email already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {'error': 'User with this email already exists'}, 409

            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            
           # Refresh the new_user object to get the auto-incremented user_id
            db.session.refresh(new_user)

            # Return the user_id in the response
            response_data = {
                'message': 'User created successfully',
                'user_id': new_user.user_id  # Assuming 'user_id' is the actual attribute name
            }
            return response_data, 201
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction
            return {'error': 'Error creating user'}, 500

    # Editing/Updating Data
    def put(self, email_or_user_id=None):
        if email_or_user_id:
            if re.match(r'^[\w\.-]+@[\w\.-]+$', email_or_user_id):
                user = User.query.filter(User.email == email_or_user_id).first()
            else:
                user = User.query.get(email_or_user_id)
            if user:
                data = request.get_json()
                if 'first_name' in data:
                    user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                if 'mobile_number' in data:
                    user.mobile_number = data['mobile_number']
                if 'user_type' in data:
                    user.user_type = data['user_type']
                if 'is_validated' in data: 
                    user.is_validated = data['is_validated']
                if 'lessor_id' in data:
                    user.lessor_id = data['lessor_id']
                db.session.commit()
                return {'message': 'User updated successfully'}
            else:
                return {'message': 'User not found'}, 404

    # Delete Data
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return {'message': 'User not found'}, 404