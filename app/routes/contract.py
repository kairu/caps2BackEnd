import os
from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contract/<filename>', methods=['GET'])
def serve_contract(filename):
    if current_app.config['CONTRACTS']:
        return send_from_directory(current_app.config['CONTRACTS'], filename, mimetype=get_mimetype(filename))
    
@contract_bp.route('/contract', methods=['POST'])
def store_contract_image():
    if current_app.config['CONTRACTS']:
        if request.method == 'POST':
            file = request.files['file']
            hashed_filename = hash_filename(file.filename)
            filepath = f'{current_app.config["CONTRACTS"]}/{hashed_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hashed_filename}, 200