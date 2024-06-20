from typing import Tuple

from flask import Blueprint, request, jsonify, Response
from src.routes.repository import add_order, get_orders, edit_order, delete_order, get_order, update_status
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
