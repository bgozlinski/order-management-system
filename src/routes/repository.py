from src.database.models import Order
from src.database.db import get_db
from src.schemas.orders import OrderSchema
from datetime import datetime


def add_order(order: OrderSchema):
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


def get_orders():
    db = next(get_db())
    orders = db.query(Order).all()
    return orders
