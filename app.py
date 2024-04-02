from flask import request
from creation import app, api, startup, send_from_directory
# Define Resources
from crud_resource import UserResource, UnitResource, TenantResource, LeaseAgreementResource, PaymentResource, BillResource, CmsResource, AccessControlResource
import pathlib
from enums import MIMETYPES

# Add Resources to the API
api.add_resource(UserResource, '/user', '/user/<string:email_or_user_id>')
api.add_resource(UnitResource, '/unit', '/unit/<int:unit_id>')
api.add_resource(TenantResource, '/tenant', '/tenant/<int:tenant_id>')
api.add_resource(LeaseAgreementResource, '/lease', '/lease/<int:lease_agreement_id>')
api.add_resource(PaymentResource, '/payment', '/payment/<int:payment_id>')
api.add_resource(BillResource, '/bill', '/bill/<int:bill_id>')
api.add_resource(CmsResource, '/cms', '/cms/<int:cms_id>')
api.add_resource(AccessControlResource, '/accesscontrol')


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
    
def get_mimetype(filename):
    return MIMETYPES.get(pathlib.Path(filename.lower()).suffix, 'application/octet-stream')

import hashlib
import os
@app.route('/bulletin', methods=['POST'])
def store_bulletin_image():
    if app.config['BULLETIN_IMAGES']:
        if request.method == 'POST':
            file = request.files['file']
            hash_filename = hashlib.sha256(file.filename.encode('utf-8')).hexdigest()
            hash_filename += pathlib.Path(file.filename).suffix
            filepath = f'{app.config["BULLETIN_IMAGES"]}/{hash_filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
            file.save(filepath)
            return {'file': hash_filename}, 200

