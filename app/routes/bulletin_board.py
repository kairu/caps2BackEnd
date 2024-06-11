from common import Blueprint, send_from_directory, current_app, os, request, get_mimetype, hash_filename



bulletin_bp = Blueprint('bulletin', __name__)

@bulletin_bp.route('/bulletin/<filename>', methods=['GET'])
def serve_image(filename):
    if current_app.config['BULLETIN_IMAGES']:
        return send_from_directory(current_app.config['BULLETIN_IMAGES'], filename, mimetype=get_mimetype(filename))

@bulletin_bp.route('/bulletin', methods=['POST'])
def store_bulletin_image():
    if current_app.config['BULLETIN_IMAGES']:
        if request.method == 'POST':
            file = request.files['file']
            hashed_filename = hash_filename(file.filename)
            filepath = f'{current_app.config["BULLETIN_IMAGES"]}/{hashed_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hashed_filename}, 200