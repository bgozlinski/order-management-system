import os
from typing import Tuple

from flask import Blueprint, request, jsonify, send_file, Response
from src.routes.services import export_orders_to_hdf5, import_orders_from_hdf5

hdf5_bp = Blueprint('hdf5', __name__)


@hdf5_bp.route('/orders/export/hdf5', methods=['GET'])
def export_orders_to_hdf5_endpoint() -> Response | Tuple[Response, int]:
    """
    API endpoint to export orders to an HDF5 file.

    This endpoint calls the export_orders_to_hdf5 function to create the HDF5 file,
    then sends the file as an attachment for download.

    Returns:
        Response: A Flask response object that sends the HDF5 file as an attachment.
    """
    try:
        file_path = export_orders_to_hdf5()
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@hdf5_bp.route('/orders/import/hdf5', methods=['POST'])
def import_orders_from_hdf5_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to import orders from an HDF5 file.

    This endpoint reads the HDF5 file from the request, saves it to the 'uploads' directory,
    and calls the import_orders_from_hdf5 function to import the orders.

    Returns:
        Tuple[Response, int]: A Flask response object with a success message.
    """
    try:
        file = request.files['file']
        file_path = os.path.join('uploads', file.filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file.save(file_path)
        import_orders_from_hdf5(file_path)
        return jsonify({"message": "Orders imported successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
