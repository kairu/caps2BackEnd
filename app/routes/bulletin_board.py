import os
from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename

bulletin_bp = Blueprint('bulletin', __name__)

@bulletin_bp.route('/bulletin/<filename>', methods=['GET'])
def serve_image(filename):
    bulletin_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['BULLETIN_IMAGES']))
    full_file_path = os.path.normpath(os.path.join(bulletin_images_path, filename))
    if os.path.exists(full_file_path):
        return send_from_directory(bulletin_images_path, filename, mimetype=get_mimetype(filename))
    return "File not found", 404

@bulletin_bp.route('/bulletin', methods=['POST'])
def store_bulletin_image():
    bulletin_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['BULLETIN_IMAGES']))
    if request.method == 'POST':
        file = request.files['file']
        hashed_filename = hash_filename(file.filename)
        filepath = os.path.normpath(os.path.join(bulletin_images_path, hashed_filename))
        if os.path.exists(filepath):
            os.remove(filepath)
        file.save(filepath)
        return {'file': hashed_filename}, 200
    return "Invalid request", 400