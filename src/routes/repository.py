from typing import List, Optional, Union, Dict
from src.database.models import Order
from src.database.db import get_db
from src.schemas.orders import OrderSchema
from datetime import datetime


def add_order(order: OrderSchema) -> Order:
    """
    Adds a new order to the database.

    Args:
        order (OrderSchema): The order details to be added.

    Returns:
        Order: The newly created order object.
    """
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
    """
    Retrieves all orders from the database.

    Returns:
        List[Order]: A list of all orders.
    """
    db = next(get_db())
    orders = db.query(Order).all()
    return orders


def get_order(id: int) -> Optional[Order]:
    """
    Retrieves a single order by its ID.

    Args:
        id (int): The ID of the order to retrieve.

    Returns:
        Optional[Order]: The order object if found, else None.

    Raises:
        ValueError: If the order with the given ID does not exist.
    """
    db = next(get_db())
    order = db.get(Order, id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    return order


def edit_order(id: int, updated_order: OrderSchema) -> Order:
    """
    Edits an existing order with the provided updated order details.

    Args:
        id (int): The ID of the order to be edited.
        updated_order (OrderSchema): The updated order details.

    Returns:
        Order: The updated order object.

    Raises:
        ValueError: If the order with the given ID does not exist.
    """
    db = next(get_db())
    order = db.get(Order, id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    order.name = updated_order.name
    order.description = updated_order.description
    order.status = updated_order.status
    db.commit()
    db.refresh(order)
    return order


def delete_order(id: int) -> Order:
    """
    Deletes an order by its ID.

    Args:
        id (int): The ID of the order to delete.

    Returns:
        Order: The deleted order object.

    Raises:
        ValueError: If the order with the given ID does not exist.
    """
    db = next(get_db())
    order = db.get(Order, id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    db.delete(order)
    db.commit()
    return order


def update_status(ids: List[int], new_status: str) -> Dict[str, Union[List[Order], List[str]]]:
    """
    Updates the status of multiple orders.

    Args:
        ids (List[int]): A list of order IDs to update.
        new_status (str): The new status to set for the orders.

    Returns:
        Dict[str, Union[List[Order], List[str]]]: A dictionary containing lists of updated orders and not found order IDs.
    """
    db = next(get_db())
    updated_orders = []
    not_found_orders = []

    for id in ids:
        order = db.get(Order, id)
        if order:
            order.status = new_status
            db.commit()
            db.refresh(order)
            updated_orders.append(order)
        else:
            not_found_orders.append(f"Order ID {id} not found")

    return {
        "updated_orders": updated_orders,
        "not_found_orders": not_found_orders
    }
