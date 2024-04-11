from creation import db, Payment
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class PaymentResource(Resource):
    def get(self, payment_id=None):
        if payment_id:
            payment = Payment.query.get(payment_id)
            if payment:
                return{
                    'payment_id': payment.payment_id,
                    'lease_agreement_id': payment.lease_agreement_id,
                    'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                    'amount': payment.amount,
                    'payment_method': payment.payment_method,
                    'reference_number': payment.reference_number,
                    'image_path': payment.image_path,
                    'status': payment.status.name
                }
            else:
                return { 'message': 'payment not found'}, 404
        else:
            payments = Payment.query.all()
            return [{
                'payment_id': payment.payment_id,
                'lease_agreement_id': payment.lease_agreement_id,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'reference_number': payment.reference_number,
                'image_path': payment.image_path,
                'status': payment.status.name
            }for payment in payments] 
    
    # Add data
    def post(self):
        try:
            data = request.get_json()

            # Check if Payment exists
            existing_payment = Payment.query.filter_by(reference_number=data['reference_number']).first()
            if existing_payment:
                return {'error': 'Payment reference number already exists'}, 409
            
            new_payment = Payment(**data)
            db.session.add(new_payment)
            db.session.commit()
            return {'message': 'Payment created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f'Error creating payment: {str(e)}')
            return {'error': 'Error creating payment'}, 500
    
    # Edit data
    def put(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            data = request.get_json()
            payment.payment_date = data['payment_date']
            payment.amount = data['amount']
            payment.payment_method = data['payment_method']
            payment.reference_number = data['reference_number']
            payment.image_path = data['image_path']
            payment.status = data['status']
            db.session.commit()
            return {'message': 'Payment updated successfully'}
        else:
            return {'message': 'Payment not found'}, 404

    # Prohibit delete
    def delete(self, payment_id):
        return {'message': 'Payments cannot be removed'}, 404
