from .common import Resource, request, IntegrityError
from ..models import Unit
from ..extensions import db

class UnitResource(Resource):
    def get(self, unit_id=None):
        if unit_id:
            unit = Unit.query.get(unit_id)
            if unit:
                return {
                    'unit_id': unit.unit_id,
                    'user_id': unit.user_id,
                    'tower_number': unit.tower_number,
                    'floor_number': unit.floor_number,
                    'unit_number': unit.unit_number,
                    'sq_foot': unit.sq_foot,
                    'number_of_bedrooms': unit.number_of_bedrooms,
                    'number_of_bathrooms': unit.number_of_bathrooms,
                    'parking_slot': unit.parking_slot,
                    'remaining_balance': unit.remaining_balance
                }
            else:
                return {'message': 'Unit not found'}, 404
        else:
            units = Unit.query.all()
            return [{
                'unit_id': unit.unit_id,
                'user_id': unit.user_id,
                'tower_number': unit.tower_number,
                'floor_number': unit.floor_number,
                'unit_number': unit.unit_number,
                'sq_foot': unit.sq_foot,
                'number_of_bedrooms': unit.number_of_bedrooms,
                'number_of_bathrooms': unit.number_of_bathrooms,
                'parking_slot': unit.parking_slot,
                'remaining_balance': unit.remaining_balance
            } for unit in units]
    
    # Add data
    def post(self):
        try:
            data = request.get_json()
            
            # TODO Duplicate tower, floor and unit is allowed. what to check only is??
            # Check if unit already exists
            # existing_unit = Unit.query.filter_by(tower_number=data['tower_number'], floor_number=data['floor_number'], unit_number=data['unit_number']).first()
            # if existing_unit:
            #     return {'error': 'Unit with this tower number, floor number, and unit number already exists'}, 409

            new_unit = Unit(**data)
            db.session.add(new_unit)
            db.session.commit()
            return {'message': 'Unit created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction
            print(f"Error creating unit: {str(e)}")
            return {'error': 'Error creating unit'}, 500
        
    # Edit Data    
    def put(self, unit_id):
        unit = Unit.query.get(unit_id)
        if unit:
            data = request.get_json()
            unit.tower_number = data['tower_number']
            unit.floor_number = data['floor_number']
            unit.unit_number = data['unit_number']
            if data.get('sq_foot'):
                unit.sq_foot = data['sq_foot']
            if data.get('number_of_bedrooms'):        
                unit.number_of_bedrooms = data['number_of_bedrooms']
            if data.get('number_of_bathrooms'):
                unit.number_of_bathrooms = data['number_of_bathrooms']  
            if data.get('parking_slot'):
                unit.parking_slot = data['parking_slot']
            if data.get('remaining_balance'):
                unit.remaining_balance = data['remaining_balance']

            db.session.commit()
            return {'message': 'Unit updated successfully'}
        else:
            return {'message': 'Unit not found'}, 404

    def delete(self, unit_id):
        unit = Unit.query.get(unit_id)
        if unit:
            db.session.delete(unit)
            db.session.commit()
            return {'message': 'Unit deleted successfully'}
        else:
            return {'message': 'Unit not found'}, 404