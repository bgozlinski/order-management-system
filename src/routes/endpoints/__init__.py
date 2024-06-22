from flask import Blueprint
from .crud_endpoints import crud_bp
from .report_endpoints import report_bp
from .hdf5_endpoints import hdf5_bp
from .xml_endpoints import xml_bp


api_orders_bp = Blueprint('api_orders', __name__, url_prefix='/api')


api_orders_bp.register_blueprint(crud_bp)
api_orders_bp.register_blueprint(report_bp)
api_orders_bp.register_blueprint(hdf5_bp)
api_orders_bp.register_blueprint(xml_bp)