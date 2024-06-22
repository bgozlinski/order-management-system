from typing import Tuple

from flask import Blueprint, jsonify, send_file, Response
from src.routes.services import generate_report_xlsx, get_order_statistics

report_bp = Blueprint('reports', __name__)


@report_bp.route('/orders/statistics', methods=['GET'])
def get_order_statistics_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to retrieve statistics about the orders.

    This endpoint returns statistics such as the count of each status.

    Returns:
        Tuple[Response, int]: A Flask response object with the order statistics.
    """
    try:
        statistics = get_order_statistics()
        return jsonify(statistics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route('/orders/report', methods=['GET'])
def generate_report_endpoint() -> Response | Tuple[Response, int]:
    """
    API endpoint to generate an XLSX report containing all orders in the system.

    This endpoint calls the generate_report_xlsx function to create the report,
    then sends the report file as an attachment for download.

    Returns:
        Response: A Flask response object that sends the XLSX report as an attachment.
    """
    try:
        report_path = generate_report_xlsx()
        return send_file(report_path, as_attachment=True, download_name='orders_report.xlsx')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
