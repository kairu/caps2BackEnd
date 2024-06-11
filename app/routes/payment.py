from common import Blueprint, send_from_directory, current_app, os, request, get_mimetype, hash_filename

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/paymentImage/<filename>', methods=['GET'])
def serve_payment_image(filename):
    if current_app.config['PAYMENT_IMAGES']:
        return send_from_directory(current_app.config['PAYMENT_IMAGES'], filename, mimetype=get_mimetype(filename))
  
@payment_bp.route('/paymentImage', methods=['POST'])
def store_payment_image():
    if current_app.config['PAYMENT_IMAGES']:
        if request.method == 'POST':
            file = request.files['file']
            hashed_filename = hash_filename(file.filename)
            filepath = f'{current_app.config["PAYMENT_IMAGES"]}/{hashed_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hashed_filename}, 200