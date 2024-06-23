from typing import Dict

import pandas as pd

from src.database.db import get_db
from src.database.models import Order


def get_order_statistics() -> Dict[str, str]:
    """
    Retrieves statistics about the orders, such as the count of each status.

    Returns:
        Dict[str, str]: A dictionary with order status counts.
    """
    db = next(get_db())
    orders = db.query(Order).all()

    # Convert orders to a list of dictionaries and then to a DataFrame
    data = [order.to_dict() for order in orders]
    df = pd.DataFrame(data)

    # Count the occurrences of each status
    status_counts = df['status'].value_counts().to_dict()

    return status_counts
