from flask import request
from creation import app, api, startup, send_from_directory
import ocr
# Define Resources
from crud_resource import UserResource, UnitResource, LeaseAgreementResource, PaymentResource, BillResource, CmsResource, AccessControlResource
import pathlib
from enums import MIMETYPES
import requests

# Add Resources to the API
api.add_resource(UserResource, '/user', '/user/<string:email_or_user_id>')
api.add_resource(UnitResource, '/unit', '/unit/<int:unit_id>')
# api.add_resource(TenantResource, '/tenant', '/tenant/<int:tenant_id>')
api.add_resource(LeaseAgreementResource, '/lease', '/lease/<int:lease_agreement_id>')
api.add_resource(PaymentResource, '/payment', '/payment/<int:payment_id>')
api.add_resource(BillResource, '/bill', '/bill/<int:bill_id>')
api.add_resource(CmsResource, '/cms', '/cms/<int:cms_id>')
api.add_resource(AccessControlResource, '/accesscontrol')

def get_mimetype(filename):
    return MIMETYPES.get(pathlib.Path(filename.lower()).suffix, 'application/octet-stream')

# Temporary 
@app.route('/')
def index():
    startup()
    # print(f'Date is: {datetime.now().date()}')
    # print(f'Time is: {datetime.now().time()}')
    return 'Hello World!'

@app.route('/bulletin/<filename>', methods=['GET'])
def serve_image(filename):
    if app.config['BULLETIN_IMAGES']:
        return send_from_directory(app.config['BULLETIN_IMAGES'], filename, mimetype=get_mimetype(filename))

@app.route('/contract/<filename>', methods=['GET'])
def serve_contract(filename):
    if app.config['CONTRACTS']:
        return send_from_directory(app.config['CONTRACTS'], filename, mimetype=get_mimetype(filename))
    
@app.route('/ocr/<filename>', methods=['GET'])
def serve_ocr_receipt(filename):
    if app.config['OCR_RECEIPTS']:
        return send_from_directory(app.config['OCR_RECEIPTS'], filename, mimetype=get_mimetype(filename))
    
import hashlib
import os
@app.route('/bulletin', methods=['POST'])
def store_bulletin_image():
    if app.config['BULLETIN_IMAGES']:
        if request.method == 'POST':
            file = request.files['file']
            hash_filename = hash_filename(file.filename)
            filepath = f'{app.config["BULLETIN_IMAGES"]}/{hash_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hash_filename}, 200
        
@app.route('/contract', methods=['POST'])
def store_contract_image():
    if app.config['CONTRACTS']:
        if request.method == 'POST':
            file = request.files['file']
            hash_filename = hash_filename(file.filename)
            filepath = f'{app.config["CONTRACTS"]}/{hash_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hash_filename}, 200

import json
@app.route('/ocr', methods=['POST'])
def ocr_image():
    if app.config['TEMP']:
        if request.method == 'POST':
            file = request.files['file']
            data = json.loads(request.form.get('data'))
            soa_id = str(data.get("SOA ID"))
            amount = str(data.get("Amount"))
            bill_id = data.get("bill_id")
            if '.' not in amount:
                amount = f"{amount}.00"
            amount = "{:,.2f}".format(float(amount.replace(",", "")))
            hashed_filename = hash_filename(file.filename)
            filepath = f'{app.config["TEMP"]}/{hashed_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            _backendUrl = 'http://127.0.0.1:5000'
    if ocr.process_ocr(filepath, soa_id, amount):
        if app.config['OCR_RECEIPTS']:
            if os.path.exists(f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}'):
                os.remove(f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}')
            os.rename(filepath, f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}')
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
            if app.config['OCR_RECEIPTS']:
                if os.path.exists(f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}'):
                    os.remove(f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}')
                os.rename(filepath, f'{app.config["OCR_RECEIPTS"]}/{hashed_filename}')
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
    
def hash_filename(filename):
    hash_filename = hashlib.sha256((filename + str(os.urandom(10))).encode('utf-8')).hexdigest()
    hash_filename += pathlib.Path(filename).suffix
    return hash_filename
    