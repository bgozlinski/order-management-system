import os
from typing import List, Optional, Union, Tuple, Dict
from src.database.models import Order
from src.database.db import get_db
from src.schemas.orders import OrderSchema
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill


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
    db = next(get_db())
    order = db.get(Order, id)
    if order is None:
        raise ValueError(f'Order {id} not found')
    db.delete(order)
    db.commit()
    return order


def update_status(ids: List[int], new_status: str) -> Dict[str, Union[List[Order], List[str]]]:
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


def get_order_statistics() -> Dict[str, str]:
    db = next(get_db())
    orders = db.query(Order).all()

    data = [order.to_dict() for order in orders]
    df = pd.DataFrame(data)

    status_counts = df['status'].value_counts().to_dict()

    return status_counts


def generate_report_xlsx() -> str:
    """
    Generates an XLSX report containing all orders in the system.

    This function queries the database for all orders, converts the data to a DataFrame,
    creates an Excel workbook with a sheet containing the order data, and colors the rows
    based on the order status:
        - "New" orders are colored blue.
        - "In Progress" orders are colored yellow.
        - "Completed" orders are colored green.

    The generated report is saved in the 'reports' directory.

    Returns:
        str: The file path of the generated XLSX report.
    """
    db = next(get_db())
    orders = db.query(Order).all()

    data = [order.to_dict() for order in orders]
    if not data:
        raise ValueError("No orders found to generate report.")

    df = pd.DataFrame(data)

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    headers = df.columns.tolist()
    ws.append(headers)

    status_colors = {
        "New": "0000FF",  # Blue
        "In Progress": "FFFF00",  # Yellow
        "Completed": "00FF00"  # Green
    }

    for index, row in df.iterrows():
        ws.append(row.tolist())
        status = row['status']
        fill = PatternFill(start_color=status_colors.get(status, "FFFFFF"),
                           end_color=status_colors.get(status, "FFFFFF"), fill_type="solid")
        for cell in ws[index + 2]:
            cell.fill = fill

    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    report_path = os.path.join(reports_dir, "orders_report.xlsx")
    wb.save(report_path)

    return report_path
