import os
import h5py
import pandas as pd
from src.database.db import get_db
from src.database.models import Order


def export_orders_to_hdf5() -> str:
    """
    Export all orders to an HDF5 file.

    This function retrieves all orders from the database, converts the data into a DataFrame,
    converts datetime columns to strings, and saves the data to an HDF5 file in the 'reports' directory.

    Returns:
        str: The file path of the created HDF5 file.
    """
    db = next(get_db())
    orders = db.query(Order).all()

    data = [order.to_dict() for order in orders]
    df = pd.DataFrame(data)

    for column in df.select_dtypes(include=['datetime64[ns]']).columns:
        df[column] = df[column].astype(str)

    reports_dir = os.path.join(os.getcwd(), 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    file_path = os.path.join(reports_dir, "orders.hdf5")

    with h5py.File(file_path, 'w') as f:
        for column in df.columns:
            f.create_dataset(column, data=df[column].values)

    return file_path


def import_orders_from_hdf5(file_path: str) -> None:
    """
    Import orders from an HDF5 file.

    This function reads order data from an HDF5 file, converts the data into a DataFrame,
    decodes byte strings, converts appropriate columns back to datetime, and merges the data into the database.

    Args:
        file_path (str): The file path of the HDF5 file to import.
    """
    db = next(get_db())

    with h5py.File(file_path, 'r') as f:
        data = {key: f[key][:] for key in f.keys()}

    df = pd.DataFrame(data)

    # Convert string columns back to datetime
    for column in df.columns:
        if df[column].dtype == object:
            try:
                df[column] = pd.to_datetime(df[column].astype(str), errors='ignore')
            except ValueError:
                pass

    for _, row in df.iterrows():
        order = Order(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            creation_date=row['creation_date'],
            status=row['status']
        )
        db.merge(order)
    db.commit()
