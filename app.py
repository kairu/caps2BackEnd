from creation import app, api, startup
# Define Resources
from crud_resource import UserResource, UnitResource, TenantResource, LeaseAgreementResource, PaymentResource, BillResource, CmsResource

# Add Resources to the API
api.add_resource(UserResource, '/user', '/user/<string:email>')
api.add_resource(UnitResource, '/unit', '/unit/<int:unit_id>')
api.add_resource(TenantResource, '/tenant', '/tenant/<int:tenant_id>')
api.add_resource(LeaseAgreementResource, '/lease', '/lease/<int:lease_agreement_id>')
api.add_resource(PaymentResource, '/payment', '/payment/<int:payment_id>')
api.add_resource(BillResource, '/bill', '/bill/<int:bill_id>')
api.add_resource(CmsResource, '/cms', '/cms/<int:cms_id>')

# Temporary 
@app.route('/')
def index():
    startup()
    return 'Hello World!'
