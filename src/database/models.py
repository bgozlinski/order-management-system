"""
This module defines the SQLAlchemy ORM model for the 'Order' entity and provides a utility
method to convert the model instances to dictionaries.

Classes:
    Order: Represents the 'orders' table in the database with columns for id, name, description, creation_date, and status.

Usage:
    Import this module to define and interact with the 'Order' table in the database.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Order(Base):
    """
    Represents the 'orders' table in the database.

    Attributes:
        id (int): The primary key of the order.
        name (str): The name of the order.
        description (str): A description of the order.
        creation_date (datetime): The creation date of the order, defaults to the current UTC datetime.
        status (str): The status of the order.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    creation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)

    def to_dict(self) -> dict:
        """
        Converts the Order instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Order instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date,
            'status': self.status
        }
