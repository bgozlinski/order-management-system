import os
from typing import Tuple

from flask import Blueprint, request, jsonify, send_file, Response
from src.routes.services import export_orders_to_xml, import_orders_from_xml

xml_bp = Blueprint('xml', __name__)


@xml_bp.route('/orders/export/xml', methods=['GET'])
def export_orders_to_xml_endpoint() -> Response | Tuple[Response, int]:
    """
    API endpoint to export orders to an XML file.

    This endpoint calls the export_orders_to_xml function to create the XML file,
    then sends the file as an attachment for download.

    Returns:
        Response: A Flask response object that sends the XML file as an attachment.
    """
    try:
        file_path = export_orders_to_xml()
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@xml_bp.route('/orders/import/xml', methods=['POST'])
def import_orders_from_xml_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to import orders from an XML file.

    This endpoint reads the XML file from the request, saves it to the 'uploads' directory,
    and calls the import_orders_from_xml function to import the orders.

    Returns:
        Tuple[Response, int]: A Flask response object with a success message.
    """
    try:
        file = request.files['file']
        file_path = os.path.join('uploads', file.filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save(file_path)
        import_orders_from_xml(file_path)
        return jsonify({"message": "Orders imported successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
