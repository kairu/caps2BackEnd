from creation import db, User
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class UserResource(Resource):
    # Get Data
    def get(self, email=None):
        if email:
            user = User.query.filter(User.email == email).first()
            if user:
                user_data = {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'mobile_number': user.mobile_number,
                    'user_type': user.user_type.name,
                    'is_active': user.is_active,
                    'is_validated': user.is_validated
                }

                # Adding relationships data
                if user.unit:
                    user_data['units'] = [{
                        'unit_id': unit.unit_id,
                        'tower_number': unit.tower_number,
                        'floor_number': unit.floor_number,
                        'unit_number': unit.unit_number,
                        'sq_foot': unit.sq_foot,
                        'number_of_bedrooms': unit.number_of_bedrooms,
                        'number_of_bathrooms': unit.number_of_bathrooms,
                        'parking_slot': unit.parking_slot,
                        'remaining_balance': unit.remaining_balance,
                        'bills': [{
                            'bill_id': bill.bill_id,
                            'month': bill.month.name,
                            'due_date': bill.due_date.isoformat() if bill.due_date else None,
                            'total_amount': bill.total_amount,
                            'breakdown': bill.breakdown,
                            'bill_type': bill.bill_type.name,
                            'payment_method': bill.payment_method,
                            'status': bill.status.name
                        } for bill in unit.bills]
                    } for unit in user.unit]

                if user.tenants:
                    user_data['tenants'] = [{
                        'tenant_id': tenant.tenant_id,
                        'move_in_date': tenant.move_in_date.isoformat() if tenant.move_in_date else None,
                        'move_out_date': tenant.move_out_date.isoformat() if tenant.move_out_date else None
                    } for tenant in user.tenants]

                if user.lease_agreements:
                    user_data['lease_agreements'] = [{
                        'lease_agreement_id': agreement.lease_agreement_id,
                        'unit_id': agreement.unit_id,
                        'start_date': agreement.start_date.isoformat() if agreement.start_date else None,
                        'end_date': agreement.end_date.isoformat() if agreement.end_date else None,
                        'monthly_rent': agreement.monthly_rent,
                        'security_deposit': agreement.security_deposit
                    } for agreement in user.lease_agreements]

                if user.payments:
                    user_data['payments'] = [{
                        'payment_id': payment.payment_id,
                        'unit_id': payment.unit_id,
                        'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                        'amount': payment.amount,
                        'payment_method': payment.payment_method,
                        'reference_number': payment.reference_number,
                        'status': payment.status.name
                    } for payment in user.payments]

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
                        'archive': cms.archive
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
                    'is_validated': user.is_validated
                }

                # Adding relationships data
                if user.unit:
                    user_data['units'] = [{
                        'unit_id': unit.unit_id,
                        'tower_number': unit.tower_number,
                        'floor_number': unit.floor_number,
                        'unit_number': unit.unit_number,
                        'sq_foot': unit.sq_foot,
                        'number_of_bedrooms': unit.number_of_bedrooms,
                        'number_of_bathrooms': unit.number_of_bathrooms,
                        'parking_slot': unit.parking_slot,
                        'remaining_balance': unit.remaining_balance,
                        'bills': [{
                            'bill_id': bill.bill_id,
                            'month': bill.month.name,
                            'due_date': bill.due_date.isoformat() if bill.due_date else None,
                            'total_amount': bill.total_amount,
                            'breakdown': bill.breakdown,
                            'bill_type': bill.bill_type.name,
                            'payment_method': bill.payment_method,
                            'status': bill.status.name
                        } for bill in unit.bills]
                    } for unit in user.unit]

                if user.tenants:
                    user_data['tenants'] = [{
                        'tenant_id': tenant.tenant_id,
                        'move_in_date': tenant.move_in_date.isoformat() if tenant.move_in_date else None,
                        'move_out_date': tenant.move_out_date.isoformat() if tenant.move_out_date else None
                    } for tenant in user.tenants]

                if user.lease_agreements:
                    user_data['lease_agreements'] = [{
                        'lease_agreement_id': agreement.lease_agreement_id,
                        'unit_id': agreement.unit_id,
                        'start_date': agreement.start_date.isoformat() if agreement.start_date else None,
                        'end_date': agreement.end_date.isoformat() if agreement.end_date else None,
                        'monthly_rent': agreement.monthly_rent,
                        'security_deposit': agreement.security_deposit
                    } for agreement in user.lease_agreements]

                if user.payments:
                    user_data['payments'] = [{
                        'payment_id': payment.payment_id,
                        'unit_id': payment.unit_id,
                        'payment_date': payment.payment_date,
                        'amount': payment.amount,
                        'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                        'reference_number': payment.reference_number,
                        'status': payment.status.name
                    } for payment in user.payments]

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
                        'archive': cms.archive
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
            print(f"Error creating user: {str(e)}")
            return {'error': 'Error creating user'}, 500

    # Editing/Updating Data
    def put(self, email=None):
        if email:
            user = User.query.filter(User.email == email).first()
            if user:
                data = request.get_json()
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.mobile_number = data['mobile_number']
                if data.get('user_type'):
                    user.user_type = data['user_type']
                user.is_validated = data['is_validated']
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