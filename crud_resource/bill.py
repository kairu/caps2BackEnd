from creation import db, Bill
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

class BillResource(Resource):
    def get(self, bill_id=None):
        if bill_id:
            bill = Bill.query.get(bill_id)
            if bill:
                return{
                    'bill_id': bill.bill_id,
                    'unit_id': bill.unit_id,
                    'month': bill.month.name,
                    'due_date': bill.due_date.isoformat() if bill.due_date else None,
                    'total_amount': bill.total_amount,
                    'breakdown': bill.breakdown,
                    'status': bill.status.name
                }
            else:
                return {'message': 'Bill not found'}, 404
        else:
            bills = Bill.query.all()
            return [{
                'bill_id': bill.bill_id,
                'unit_id': bill.unit_id,
                'month': bill.month.name,
                'due_date': bill.due_date.isoformat() if bill.due_date else None,
                'total_amount': bill.total_amount,
                'breakdown': bill.breakdown,
                'bill_type': bill.bill_type,
                'payment_method': bill.payment_method,
                'status': bill.status.name
            } for bill in bills]
        
    # Add Data
    def post(self):
        try:
            data = request.get_json()

            # Check if bill already exsists
            existing_bill = Bill.query.filter_by(unit_id=data['unit_id'], month=data['month'],total_amount=data['total_amount']).first()
            if existing_bill:
                return{'error': 'Bill already exists'},409
            
            new_bill = Bill(**data)
            db.session.add(new_bill)
            db.session.commit()
            return {'message': 'Bill created successfully'},201
        except IntegrityError as e:
            db.session.rollback()
            print(f'Error creating bill: {str(e)}')
            return {'error': 'Error creating bill'}, 500
    
    # Edit Data
    def put(self, bill_id):
        bill = Bill.query.get(bill_id)
        if bill:
            data = request.get_json()
            bill.unit_id = data['unit_id']
            bill.month = data['month']
            bill.due_date = data['due_date']
            bill.total_amount = data['total_amount']
            bill.breakdown = data['breakdown']
            bill.type = data['type']
            bill.payment_method = data['payment_method']
            bill.status = data['status']
            db.session.commit()
            return {'message': 'Bill updated successfully'}
        else:
            return {'error': 'Error updating bill'}, 404
        
    # Prohibit deletion of a bill
    def delete(self, bill_id):
        return {'message': 'Bill cannot be removed'}, 404