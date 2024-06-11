import json
from ..extensions import db
from ..models import User, Cms, Unit, Bill, LeaseAgreement, Payment, AccessControl

def load_data_to_db(model, json_file_path, filter_key, filter_value):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        existing_entry = model.query.filter_by(**{filter_key: item[filter_key]}).first()
        if existing_entry is None:
            entry = model(**item)
            db.session.add(entry)

    print(f'{model.__name__} has been populated!')
    db.session.commit()

def startup():
    # List of models to iterate over
    models = [
        {'model': User, 'filter_key': 'user_id'},
        {'model': Cms, 'filter_key': 'cms_id'},
        # {'model': Tenant, 'filter_key': 'tenant_id'},
        {'model': Unit, 'filter_key': 'unit_id'},
        {'model': Bill, 'filter_key': 'bill_id'},
        {'model': LeaseAgreement, 'filter_key': 'lease_agreement_id'},
        {'model': Payment, 'filter_key': 'payment_id'},
        {'model': AccessControl, 'filter_key': 'module_id'},
    ]

    # Iterate over models and load data
    for model_info in models:
        model = model_info['model']
        filter_key = model_info['filter_key']
        model_name = model.__name__.lower()  # Convert class name to lowercase string
        load_data_to_db(model, f'dummydata/{model_name}s.json', filter_key, None)