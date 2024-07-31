from .common import Resource, request, IntegrityError
from ..models import Payment
from ..extensions import db

class PaymentResource(Resource):
    def get(self, agreement_or_payment_id=None):
        if agreement_or_payment_id:
            if agreement_or_payment_id.isdigit():
                payments = Payment.query.get(agreement_or_payment_id)
                payments = [payments] if payments else []
            else:
                agreement_or_payment_id = int(agreement_or_payment_id.replace('LEASE', '').strip())
                payments = Payment.query.filter_by(lease_agreement_id=agreement_or_payment_id)
            if payments:
                return[{
                    'payment_id': payment.payment_id,
                    'lease_agreement_id': payment.lease_agreement_id,
                    'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                    'amount': payment.amount,
                    'payment_method': payment.payment_method,
                    'reference_number': payment.reference_number,
                    'image_path': payment.image_path,
                    'status': payment.status.name
                } for payment in payments]
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
            # existing_payment = Payment.query.filter_by(reference_number=data['reference_number']).first()
            # if existing_payment:
                # return {'error': 'Payment reference number already exists'}, 409
            
            new_payment = Payment(**data)
            db.session.add(new_payment)
            db.session.commit()
            return {'message': 'Payment created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f'Error creating payment: {str(e)}')
            return {'error': 'Error creating payment'}, 500
    
    # Edit data
    def put(self, agreement_or_payment_id):
        if agreement_or_payment_id.isdigit():
                payment = Payment.query.get(agreement_or_payment_id)
        else:
            agreement_or_payment_id = int(agreement_or_payment_id.replace('LEASE', '').strip())
            payment = Payment.query.filter_by(lease_agreement_id=agreement_or_payment_id)
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
    def delete(self, lease_agreement_id):
        return {'message': 'Payments cannot be removed'}, 404
