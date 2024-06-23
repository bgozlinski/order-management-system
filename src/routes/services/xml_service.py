import os

import pandas as pd

from src.database.db import get_db
from src.database.models import Order
import xml.etree.ElementTree as ET

def export_orders_to_xml() -> str:
    """
    Export all orders to an XML file.

    This function retrieves all orders from the database and saves the data to an XML file in the 'reports' directory.

    Returns:
        str: The file path of the created XML file.
    """
    db = next(get_db())
    orders = db.query(Order).all()

    root = ET.Element("orders")
    for order in orders:
        order_elem = ET.Element("order")
        for key, value in order.to_dict().items():
            child = ET.Element(key)
            child.text = str(value)
            order_elem.append(child)
        root.append(order_elem)

    tree = ET.ElementTree(root)

    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    file_path = os.path.join(reports_dir, "orders.xml")
    tree.write(file_path)

    return file_path


def import_orders_from_xml(file_path: str) -> None:
    """
    Import orders from an XML file.

    This function reads order data from an XML file and merges the data into the database.

    Args:
        file_path (str): The file path of the XML file to import.
    """
    db = next(get_db())

    tree = ET.parse(file_path)
    root = tree.getroot()

    for order_elem in root.findall('order'):
        order_data = {child.tag: child.text for child in order_elem}
        order_data['id'] = int(order_data['id'])
        order_data['creation_date'] = pd.to_datetime(order_data['creation_date'])

        order = Order(
            id=order_data['id'],
            name=order_data['name'],
            description=order_data['description'],
            creation_date=order_data['creation_date'],
            status=order_data['status']
        )
        db.merge(order)
    db.commit()
