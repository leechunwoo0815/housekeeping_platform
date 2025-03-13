from flask import Blueprint
marketing_bp = Blueprint('marketing',__name__, url_prefix = '/marketing')
from . import routes
