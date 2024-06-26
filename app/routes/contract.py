import os
from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contract/<filename>', methods=['GET'])
def serve_contract(filename):
    contract_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['CONTRACTS']))
    full_file_path = os.path.normpath(os.path.join(contract_images_path, filename))
    if os.path.exists(full_file_path):
        return send_from_directory(contract_images_path, filename, mimetype=get_mimetype(filename))
    return "File not found", 404
    
@contract_bp.route('/contract', methods=['POST'])
def store_contract_image():
    contract_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['CONTRACTS']))
    if request.method == 'POST':
        file = request.files['file']
        hashed_filename = hash_filename(file.filename)
        filepath = os.path.normpath(os.path.join(contract_images_path, hashed_filename))
        if os.path.exists(filepath):
            os.remove(filepath)
        file.save(filepath)
        return {'file': hashed_filename}, 200
    return "Invalid request", 400