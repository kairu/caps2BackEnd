import re
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime