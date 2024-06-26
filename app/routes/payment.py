import os
from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/paymentImage/<filename>', methods=['GET'])
def serve_payment_image(filename):
    payment_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['PAYMENT_IMAGES']))
    full_file_path = os.path.normpath(os.path.join(payment_images_path, filename))
    if os.path.exists(full_file_path):
        return send_from_directory(payment_images_path, filename, mimetype=get_mimetype(filename))
    return "File not found", 404
  
@payment_bp.route('/paymentImage', methods=['POST'])
def store_payment_image():
    payment_images_path = os.path.normpath(os.path.join(current_app.root_path, current_app.config['PAYMENT_IMAGES']))
    if request.method == 'POST':
        file = request.files['file']
        hashed_filename = hash_filename(file.filename)
        filepath = os.path.normpath(os.path.join(payment_images_path, hashed_filename))
        if os.path.exists(filepath):
            os.remove(filepath)
        file.save(filepath)
        return {'file': hashed_filename}, 200
    return "Invalid request", 400