from flask import Blueprint
from ..services.data_populate import startup

populate_bp = Blueprint('populate', __name__)

@populate_bp.route('/', methods=['GET'])
def index():
    startup()
    return 'Hello World!'
