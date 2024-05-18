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
                    'month': bill.month.name if bill.month else None,
                    'soa_id': bill.soa_id,
                    'due_date': bill.due_date.isoformat() if bill.due_date else None,
                    'total_amount': bill.total_amount,
                    'delinquent_amount': bill.delinquent_amount,
                    'breakdown': bill.breakdown,
                    'bill_type': bill.bill_type,
                    'payment_method': bill.payment_method,
                    'image_path': bill.image_path,
                    'status': bill.status.name
                }
            else:
                return {'message': 'Bill not found'}, 404
        else:
            bills = Bill.query.all()
            return [{
                'bill_id': bill.bill_id,
                'unit_id': bill.unit_id,
                'month': bill.month.name if bill.month else None,
                'soa_id': bill.soa_id,
                'due_date': bill.due_date.isoformat() if bill.due_date else None,
                'total_amount': bill.total_amount,
                'delinquent_amount': bill.delinquent_amount,
                'breakdown': bill.breakdown,
                'bill_type': bill.bill_type,
                'payment_method': bill.payment_method,
                'image_path': bill.image_path,
                'status': bill.status.name
            } for bill in bills]
        
    # Add Data
    def post(self):
        try:
            data = request.get_json()

            # Check if bill already exsists
            # existing_bill = Bill.query.filter_by(unit_id=data['unit_id'], month=data['month'],total_amount=data['total_amount']).first()
            # if existing_bill:
            #     return{'error': 'Bill already exists'},409
            
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
            if 'unit_id' in data:
                bill.unit_id = data['unit_id']
            if 'month' in data:
                bill.month = data['month']
            if 'soa_id' in data:
                bill.soa_id = data['soa_id']
            if 'due_date' in data:
                bill.due_date = data['due_date']
            if 'total_amount' in data:
                bill.total_amount = data['total_amount']
            if 'delinquent_amount' in data:
                bill.delinquent_amount = data['delinquent_amount']
            if 'breakdown' in data:
                bill.breakdown = data['breakdown']
            if 'bill_type' in data:
                bill.bill_type = data['bill_type']
            if 'payment_method' in data:
                bill.payment_method = data['payment_method']
            if 'image_path' in data:
                bill.image_path = data['image_path']
            if 'status' in data:
                bill.status = data['status']
            db.session.commit()
            return {'message': 'Bill updated successfully'}
        else:
            return {'error': 'Error updating bill'}, 404
        
    # Prohibit deletion of a bill
    def delete(self, bill_id):
        return {'message': 'Bill cannot be removed'}, 404