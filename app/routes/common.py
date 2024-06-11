from flask import Blueprint, send_from_directory, current_app, request
from ..services.mimetype import get_mimetype
from ..services.hashfile import hash_filename
import hashlib
import os
import requests
import json