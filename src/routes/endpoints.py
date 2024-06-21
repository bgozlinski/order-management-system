import os
from typing import Tuple
from flask import Blueprint, request, jsonify, Response, send_file
from src.routes.repository import (
    add_order,
    get_orders,
    edit_order,
    delete_order,
    get_order,
    update_status,
    get_order_statistics,
    generate_report_xlsx,
    export_orders_to_hdf5,
    import_orders_from_hdf5, import_orders_from_xml, export_orders_to_xml
)
from src.schemas.orders import OrderSchema
from pydantic import ValidationError

bp = Blueprint('api', __name__)


@bp.route('/orders', methods=['POST'])
def add_order_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to add a new order.

    This endpoint reads order data from the request, validates it using Pydantic,
    and adds the order to the database.

    Returns:
        Tuple[Response, int]: A Flask response object with the created order details or an error message.
    """
    try:
        data = request.get_json()
        order = OrderSchema(**data)
        response = add_order(order)
        return jsonify(response.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders', methods=['GET'])
def get_orders_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to retrieve all orders.

    This endpoint fetches all orders from the database and returns them as a JSON response.

    Returns:
        Tuple[Response, int]: A Flask response object with the list of orders.
    """
    response = get_orders()
    orders = [order.to_dict() for order in response]
    return jsonify(orders), 200


@bp.route('/orders/<int:id>', methods=['GET'])
def get_order_endpoint(id: int) -> Tuple[Response, int]:
    """
    API endpoint to retrieve a single order by its ID.

    Args:
        id (int): The ID of the order to retrieve.

    Returns:
        Tuple[Response, int]: A Flask response object with the order details or an error message.
    """
    try:
        response = get_order(id)
        if response is None:
            raise ValueError(f"Order with id {id} does not exist")
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/<int:id>', methods=['PUT'])
def edit_order_endpoint(id: int) -> Tuple[Response, int]:
    """
    API endpoint to edit an existing order with the provided updated order details.

    Args:
        id (int): The ID of the order to be edited.

    Returns:
        Tuple[Response, int]: A Flask response object with the updated order details or an error message.
    """
    try:
        data = request.get_json()
        updated_order = OrderSchema(**data)
        response = edit_order(id, updated_order)
        return jsonify(response.to_dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order_endpoint(id: int) -> Tuple[Response, int]:
    """
    API endpoint to delete an order by its ID.

    Args:
        id (int): The ID of the order to delete.

    Returns:
        Tuple[Response, int]: A Flask response object with the deleted order details or an error message.
    """
    try:
        response = delete_order(id)
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/update', methods=['PUT'])
def update_status_endpoint() -> Tuple[Response, int]:
    """
    API endpoint to update the status of multiple orders.

    This endpoint reads the order IDs and new status from the request, updates the orders,
    and returns the details of updated and not found orders.

    Returns:
        Tuple[Response, int]: A Flask response object with the details of updated and not found orders.
    """
    try:
        data = request.get_json()
        order_ids = data['order_ids']
        new_status = data['status']
        result = update_status(order_ids, new_status)

        updated_orders = [order.to_dict() for order in result["updated_orders"]]
        not_found_orders = result["not_found_orders"]

        return jsonify({
            "updated_orders": updated_orders,
            "not_found_orders": not_found_orders
        }), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


@bp.route('/orders/statistics', methods=['GET'])
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


@bp.route('/orders/report', methods=['GET'])
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


@bp.route('/orders/export/hdf5', methods=['GET'])
def export_orders_to_hdf5_endpoint() -> Response:
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


@bp.route('/orders/import/hdf5', methods=['POST'])
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


@bp.route('/orders/export/xml', methods=['GET'])
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


@bp.route('/orders/import/xml', methods=['POST'])
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
