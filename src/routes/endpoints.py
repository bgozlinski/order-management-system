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
    generate_report_xlsx
)
from src.schemas.orders import OrderSchema
from pydantic import ValidationError

bp = Blueprint('api', __name__)


@bp.route('/orders', methods=['POST'])
def add_order_endpoint() -> Tuple[Response, int]:
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
    response = get_orders()
    orders = [order.to_dict() for order in response]
    return jsonify(orders), 200


@bp.route('/orders/<int:id>', methods=['GET'])
def get_order_endpoint(id: int) -> Tuple[Response, int]:
    try:
        response = get_order(id)
        if response is None:
            raise ValueError(f"Order with id {id} does not exist")
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/<int:id>', methods=['PUT'])
def edit_order_endpoint(id: int) -> Tuple[Response, int]:
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
    try:
        response = delete_order(id)
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/update', methods=['PUT'])
def update_status_endpoint() -> Tuple[Response, int]:
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
    try:
        statistics = get_order_statistics()
        return jsonify(statistics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/orders/report', methods=['GET'])
def generate_report_endpoint() -> Response:
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
