from typing import Tuple

from flask import Blueprint, request, jsonify, Response
from src.routes.repository import add_order, get_orders, edit_order, delete_order
from src.schemas.orders import OrderSchema
from pydantic import ValidationError

bp = Blueprint('api', __name__)


@bp.route('/orders', methods=['POST'])
def add_order_endpoint() -> Tuple[Response, int]:
    try:
        data = request.get_json()
        order = OrderSchema(**data)
        response = add_order(order)
        return jsonify(OrderSchema.from_orm(response).dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders', methods=['GET'])
def get_orders_endpoint() -> Tuple[Response, int]:
    response = get_orders()
    orders = [OrderSchema.from_orm(order).dict() for order in response]
    return jsonify(orders), 200


@bp.route('/orders/<int:id>', methods=['GET'])
def get_order_endpoint(id: int) -> Tuple[Response, int]:
    try:
        data = request.get_json()
        update_order = OrderSchema(**data)
        response = edit_order(id, update_order)
        return jsonify(OrderSchema.from_orm(response).dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order_endpoint(id: int) -> Tuple[Response, int]:
    try:
        response = delete_order(id)
        return jsonify(OrderSchema.from_orm(response).dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
