from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .extensions import db, migrate
from .config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Check if the database exists, if not, create it
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    CORS(app, resources={r"/*": {"origins": ["http://localhost:4200"]}})
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    
    # Register Resources
    from .resources import UserResource, UnitResource, LeaseAgreementResource, PaymentResource, BillResource, CmsResource, AccessControlResource
    api.add_resource(UserResource, '/user', '/user/<string:email_or_user_id>')
    api.add_resource(UnitResource, '/unit', '/unit/<int:unit_id>')
    api.add_resource(LeaseAgreementResource, '/lease', '/lease/<string:lease_id_or_tenant_id>')
    api.add_resource(PaymentResource, '/payment', '/payment/<string:agreement_or_payment_id>')
    api.add_resource(BillResource, '/bill', '/bill/<int:bill_id>')
    api.add_resource(CmsResource, '/cms', '/cms/<int:cms_id>')
    api.add_resource(AccessControlResource, '/accesscontrol')
    
    from .models import User, Unit, LeaseAgreement, Payment, Bill, Cms, AccessControl
    
    # Tasks
    from .tasks import check_cms_archive, generate_delinquency
    scheduler.add_job(check_cms_archive, CronTrigger(hour=0, minute=0))
    scheduler.add_job(generate_delinquency, CronTrigger(hour=0, minute=0))
    scheduler.start()
    
    # Routes Blueprint
    from .routes import populate_bp, bulletin_bp, contract_bp, payment_bp, ocr_bp
    app.register_blueprint(populate_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(ocr_bp)
    
    return app