from flask import Blueprint, request, jsonify
from src.routes.repository import add_order, get_orders
from src.schemas.orders import OrderSchema
from pydantic import ValidationError

bp = Blueprint('api', __name__)


@bp.route('/orders', methods=['POST'])
def add_order_endpoint():
    try:
        data = request.get_json()
        order = OrderSchema(**data)
        response = add_order(order)
        return jsonify(OrderSchema.from_orm(response).dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400


@bp.route('/orders', methods=['GET'])
def get_orders_endpoint():
    response = get_orders()
    orders = [OrderSchema.from_orm(order).dict() for order in response]
    return jsonify(orders), 200
