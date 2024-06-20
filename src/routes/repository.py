from typing import List, Optional, Union, Tuple, Dict
from src.database.models import Order
from src.database.db import get_db
from src.schemas.orders import OrderSchema
from datetime import datetime


def add_order(order: OrderSchema) -> Order:
    db = next(get_db())
    new_order = Order(
        name=order.name,
        description=order.description,
        status=order.status,
        creation_date=order.creation_date or datetime.utcnow(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_orders() -> List[Order]:
    db = next(get_db())
    orders = db.query(Order).all()
    return orders


def get_order(id: int) -> Optional[Order]:
    db = next(get_db())
    order = db.query(Order).get(id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    return order


def edit_order(id: int, updated_order: OrderSchema) -> Order:
    db = next(get_db())
    order = db.query(Order).get(id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    order.name = updated_order.name
    order.description = updated_order.description
    order.status = updated_order.status
    db.commit()
    db.refresh(order)
    return order


def delete_order(id: int) -> Order:
    db = next(get_db())
    order = db.query(Order).get(id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    db.delete(order)
    db.commit()
    return order


def update_status(order_ids: List[int], new_status: str) -> Dict[str, Union[List[Order], List[str]]]:
    db = next(get_db())
    updated_orders = []
    not_found_orders = []

    for order_id in order_ids:
        order = db.query(Order).get(order_id)
        if order:
            order.status = new_status
            db.commit()
            db.refresh(order)
            updated_orders.append(order)
        else:
            not_found_orders.append(f"Order ID {order_id} not found")

    return {
        "updated_orders": updated_orders,
        "not_found_orders": not_found_orders
    }
