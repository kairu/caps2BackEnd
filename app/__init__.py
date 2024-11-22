from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
from sqlalchemy_utils import database_exists, create_database
from .routes.bulletin_board import bulletin_bp
from .routes.contract import contract_bp
from .routes.index import populate_bp
from .routes.ocr import ocr_bp
from .routes.payment import payment_bp
from .routes.delinqent_bills import delinquentBills_bp
from .routes.billing_performance import billing_performance_bp
from .extensions import db, migrate, scheduler
from .models import User, Unit, LeaseAgreement, Payment, Bill, Cms, AccessControl, FeedbackComplaintNotes

#scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:4200"]}})
    app.config.from_object(Config)
    api = Api(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Check if the database exists, if not, create it
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Register Resources
    from .resources import UserResource, UnitResource, LeaseAgreementResource, PaymentResource, BillResource, CmsResource, AccessControlResource, FeedbackComplaintNotesResource
    api.add_resource(UserResource, '/user', '/user/<string:email_or_user_id>')
    api.add_resource(UnitResource, '/unit', '/unit/<int:unit_id>')
    api.add_resource(LeaseAgreementResource, '/lease', '/lease/<string:lease_id_or_tenant_id>')
    api.add_resource(PaymentResource, '/payment', '/payment/<string:agreement_or_payment_id>')
    api.add_resource(BillResource, '/bill', '/bill/<int:bill_id>')
    api.add_resource(CmsResource, '/cms', '/cms/<int:cms_id>')
    api.add_resource(AccessControlResource, '/accesscontrol')
    api.add_resource(FeedbackComplaintNotesResource, '/feedbackcomplaintnotes', '/feedbackcomplaintnotes/<int:cms_id>')
    
    # Tasks
    from .tasks import check_cms_archive, generate_delinquency
    # Initialize the scheduler

    scheduler.init_app(app)
    scheduler.start()
    # Add jobs to the scheduler
    scheduler.add_job(id='check_cms_archive', func=check_cms_archive, trigger='cron', hour=0, minute=0)
    scheduler.add_job(id='generate_delinquency', func=generate_delinquency, trigger='cron', hour=0, minute=0)
    
    # Run task at runtime
    check_cms_archive()
    generate_delinquency()
    
    
    # Routes Blueprint
    app.register_blueprint(populate_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(delinquentBills_bp)
    app.register_blueprint(billing_performance_bp)
    
    return app
