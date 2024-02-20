from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists
from flask_cors import CORS
import json

# DB Credentials (Temporary) will move to vault or env
db_user = 'avidatrack'
db_password = 'password'
db_host = 'localhost'
db_port = '3306'
db_name = 'avida_track'

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    if not database_exists(f'mariadb+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'):
        create_database(f'mariadb+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Import your models here to avoid circular import
from models import User, Unit, Tenant, LeaseAgreement, Payment, Bill, Cms, AccessControl

# Populate the database (will be removed on production)
def load_data_to_db(model, json_file_path, filter_key, filter_value):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        existing_entry = model.query.filter_by(**{filter_key: item[filter_key]}).first()
        if existing_entry is None:
            entry = model(**item)
            db.session.add(entry)

    print(f'{model} has been populated!')
    db.session.commit()

# with app.app_context():
def startup():
    # List of models to iterate over
    models = [
        {'model': User, 'filter_key': 'user_id'},
        {'model': Cms, 'filter_key': 'cms_id'},
        {'model': Tenant, 'filter_key': 'tenant_id'},
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

if __name__ == '__main__':
    app.run(debug=True)