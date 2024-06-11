import os
from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename
import requests
import json
import app.services.ocr as ocr

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/ocr/<filename>', methods=['GET'])
def serve_ocr_receipt(filename):
    if current_app.config['OCR_RECEIPTS']:
        return send_from_directory(current_app.config['OCR_RECEIPTS'], filename, mimetype=get_mimetype(filename))
    
@ocr_bp.route('/ocr', methods=['POST'])
def ocr_image():
    if current_app.config['TEMP']:
        if request.method == 'POST':
            file = request.files['file']
            data = json.loads(request.form.get('data'))
            soa_id = str(data.get("SOA ID"))
            amount = data.get("Amount")
            delinquent_amount = data.get("Delinquent Amount")
            amount = str(amount + delinquent_amount)
            bill_id = data.get("bill_id")
            if '.' not in amount:
                amount = f"{amount}.00"
            amount = "{:,.2f}".format(float(amount.replace(",", "")))
            hashed_filename = hash_filename(file.filename)
            filepath = f'{current_app.config["TEMP"]}/{hashed_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            _backendUrl = 'http://127.0.0.1:5000'
    if ocr.process_ocr(filepath, soa_id, amount):
        if current_app.config['OCR_RECEIPTS']:
            if os.path.exists(f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}'):
                os.remove(f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}')
            os.rename(filepath, f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}')
            # Update the Bill Row Data
            updated_data ={
                'status': 'PAID',
                'image_path': hashed_filename
            }
            response = requests.put(f"{_backendUrl}/bill/{bill_id}", json=updated_data)
            return {'message': 'Success!'}, 200
    else:
        attempts = data.get('attempts')
        # 3 attempts
        if attempts > 2:
            if current_app.config['OCR_RECEIPTS']:
                if os.path.exists(f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}'):
                    os.remove(f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}')
                os.rename(filepath, f'{current_app.config["OCR_RECEIPTS"]}/{hashed_filename}')
            updated_data ={
                'status': 'REVIEW',
                'image_path': hashed_filename
            }
            response = requests.put(f"{_backendUrl}/bill/{bill_id}", json=updated_data)
            return {'message': 'Multiple attempts made, File will be Reviewed by the Admin.',
                    'attempts': attempts
                    }, 200
        else:
            os.remove(filepath)
            return {'message': 'Failed, Unable to read image clearly.'}, 404