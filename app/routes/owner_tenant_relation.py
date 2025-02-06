import os
from flask import Blueprint, jsonify, request, current_app, send_from_directory
from app.models.units import Unit
from app.models.user import User
from app.services.mimetype import get_mimetype
from ..services.hashfile import hash_filename

owner_tenant_relation_bp = Blueprint('owner_tenant_relation', __name__)

@owner_tenant_relation_bp.route('/find-owner', methods=['GET'])
def get_owner_tenant_relation():
    # Retrieve the Tower, Floor and Unit Number from the request parameters
    # Maybe get unit type also? Update soon
    tower_num = request.args.get('tower_number')
    floor_num = request.args.get('floor_number')
    unit_num = request.args.get('unit_number')
    # Query the database to get the units user_id based on tower, floor and unit number
    unit = Unit.query.filter_by(tower_number=tower_num, floor_number=floor_num, unit_number=unit_num).all()
    # print(unit)
    if unit:
        # Assuming the user_id is stored in the 'user_id' column of the Unit model
        # Search the returned units user_id This can be more than 1 and get the user information whose user_type is OWNER
        user_ids = [unit.user_id for unit in unit]
        owner_info = User.query.filter(User.user_id.in_(user_ids), User.user_type == 'OWNER').all()
        # Return the owner information as a JSON response
        return jsonify([{'user_id': owner.user_id,
                          'first_name': owner.first_name, 
                          'last_name': owner.last_name, 
                          'email': owner.email, 
                          'mobile_number': owner.mobile_number, 
                          'sq_foot': unit.sq_foot, 
                          'unit_type': unit.unit_type
                        } for owner in owner_info for unit in Unit.query.filter_by(user_id=owner.user_id).all()])    
    return jsonify({'message': 'No owner found for the given tower, floor and unit number'}), 404
    
@owner_tenant_relation_bp.route('/representative-image', methods=['POST'])
def store_representative_image():
    representative_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['TENANT_REPRESENTATIVE_IMAGES']))
    if request.method == 'POST':
        file = request.files['file']
        hashed_filename = hash_filename(file.filename)
        filepath = os.path.normpath(os.path.join(representative_images_path, hashed_filename))
        if os.path.exists(filepath):
            os.remove(filepath)
        file.save(filepath)
        return {'file': hashed_filename}, 200
    return "Invalid request", 400

@owner_tenant_relation_bp.route('/serve-representative-image/<filename>', methods=['GET'])
def serve_representative_image(filename):
    representative_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['TENANT_REPRESENTATIVE_IMAGES']))
    full_file_path = os.path.normpath(os.path.join(representative_images_path, filename))
    if os.path.exists(full_file_path):
        return send_from_directory(representative_images_path, filename, mimetype=get_mimetype(filename))
    return "File not found", 404