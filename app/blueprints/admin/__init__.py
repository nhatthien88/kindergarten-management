from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from app.blueprints.admin import routes
from app.blueprints.admin import user_routes
from app.blueprints.admin import classroom_routes
from app.blueprints.admin import fee_routes
from app.blueprints.admin import report_routes
from app.blueprints.admin import setting_routes