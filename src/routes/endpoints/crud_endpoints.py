from typing import Tuple

from flask import Blueprint, request, jsonify, Response
from src.routes.repository import add_order, get_orders, get_order, edit_order, delete_order, update_status
from src.schemas.orders import OrderSchema
from pydantic import ValidationError

crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/orders', methods=['POST'])
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


@crud_bp.route('/orders', methods=['GET'])
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


@crud_bp.route('/orders/<int:id>', methods=['GET'])
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


@crud_bp.route('/orders/<int:id>', methods=['PUT'])
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


@crud_bp.route('/orders/<int:id>', methods=['DELETE'])
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


@crud_bp.route('/orders/update', methods=['PUT'])
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
