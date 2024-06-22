# Order Management System

This is a simple Order Management System built with Flask and SQLAlchemy, using PostgreSQL as the primary database.

## Features

- Add, edit, delete, and view orders
- Export orders to HDF5 and XML files
- Import orders from HDF5 and XML files
- Generate reports in XLSX format
- API endpoints for managing orders
- Data Analysis of how many orders are in each status.

## Requirements

- Python 3.11+
- PostgreSQL
- pip (Python package installer)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/order_management_system.git
    cd order_management_system
    ```
   
2. **Create a virtual environment and activate it**:
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
   
3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
   
4. **Set up the environment variables**:

    Create a .env file in the root directory and add the following variables:
        
    ```env
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=your_postgres_db
    DB_HOST_IP=your_db_host_ip
    FLASK_CONFIG=development
    DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST_IP}:5432/${POSTGRES_DB}
    ```

## Running the Application

### Using Docker Compose

1. Ensure Docker is installed and running on your machine.

2. Use the included `docker-compose.yml` to set up the PostgreSQL database

3. Start the services:
    ```bash
    docker-compose up -d
    ```

4. Run the application**:

    ```bash
    python run.py
    ```

    The application will be available at http://127.0.0.1:5000

### Without Docker

1. Ensure PostgreSQL is installed and running on your machine.

2. Set up the database using the credentials specified in your `.env` file.

3. Run the Flask application:
    ```bash
    python run.py
    ```

## API Endpoints

### Base URL

The base URL for all endpoints is:

```
http://127.0.0.1:5000/api
```

  - [Add an Order](#add-an-order)
  - [Get All Orders](#get-all-orders)
  - [Get a Single Order](#get-a-single-order)
  - [Edit an Order](#edit-an-order)
  - [Delete an Order](#delete-an-order)
  - [Update Order Status](#update-order-status)
  - [Get Order Statistics](#get-order-statistics)
  - [Generate XLSX Report](#generate-xlsx-report)
  - [Export Orders to HDF5](#export-orders-to-hdf5)
  - [Import Orders from HDF5](#import-orders-from-hdf5)
  - [Export Orders to XML](#export-orders-to-xml)
  - [Import Orders from XML](#import-orders-from-xml)


### Add an Order

- **URL**: `/orders`
- **Method**: `POST`
- **Description**: Adds a new order to the database.
- **Request Body**:

  ```json
  {
      "name": "Test Order",
      "description": "Test Description",
      "status": "New"
  }
  ```

- **Response**:

  ```json
  {
      "id": 1,
      "name": "Test Order",
      "description": "Test Description",
      "status": "New",
      "creation_date": "2024-01-01T12:00:00"
  }
  ```

### Get All Orders

- **URL**: `/orders`
- **Method**: `GET`
- **Description**: Retrieves all orders from the database.
- **Response**:

  ```json
  [
      {
          "id": 1,
          "name": "Test Order",
          "description": "Test Description",
          "status": "New",
          "creation_date": "2024-01-01T12:00:00"
      }
  ]
  ```

### Get a Single Order

- **URL**: `/orders/{id}`
- **Method**: `GET`
- **Description**: Retrieves a single order by its ID.
- **Response**:

  ```json
  {
      "id": 1,
      "name": "Test Order",
      "description": "Test Description",
      "status": "New",
      "creation_date": "2024-01-01T12:00:00"
  }
  ```

### Edit an Order

- **URL**: `/orders/{id}`
- **Method**: `PUT`
- **Description**: Edits an existing order with the provided updated order details.
- **Request Body**:

  ```json
  {
      "name": "Updated Order",
      "description": "Updated Description",
      "status": "Completed"
  }
  ```

- **Response**:

  ```json
  {
      "id": 1,
      "name": "Updated Order",
      "description": "Updated Description",
      "status": "Completed",
      "creation_date": "2024-01-01T12:00:00"
  }
  ```

### Delete an Order

- **URL**: `/orders/{id}`
- **Method**: `DELETE`
- **Description**: Deletes an order by its ID.
- **Response**:

  ```json
  {
      "id": 1,
      "name": "Updated Order",
      "description": "Updated Description",
      "status": "Completed",
      "creation_date": "2024-01-01T12:00:00"
  }
  ```

### Update Order Status

- **URL**: `/orders/update`
- **Method**: `PUT`
- **Description**: Updates the status of multiple orders.
- **Request Body**:

  ```json
  {
      "order_ids": [1, 2, 3],
      "status": "Completed"
  }
  ```

- **Response**:

  ```json
  {
      "updated_orders": [
          {
              "id": 1,
              "name": "Order 1",
              "description": "Description 1",
              "status": "Completed",
              "creation_date": "2024-01-01T12:00:00"
          },
          {
              "id": 2,
              "name": "Order 2",
              "description": "Description 2",
              "status": "Completed",
              "creation_date": "2024-01-01T12:00:00"
          }
      ],
      "not_found_orders": ["Order ID 3 not found"]
  }
  ```

### Get Order Statistics

- **URL**: `/orders/statistics`
- **Method**: `GET`
- **Description**: Retrieves statistics about the orders, such as the count of each status.
- **Response**:

  ```json
  {
      "New": 10,
      "In Progress": 5,
      "Completed": 15
  }
  ```

### Generate XLSX Report

- **URL**: `/orders/report`
- **Method**: `GET`
- **Description**: Generates an XLSX report containing all orders in the system.
- **Response**: XLSX file download.

### Export Orders to HDF5

- **URL**: `/orders/export/hdf5`
- **Method**: `GET`
- **Description**: Exports orders to an HDF5 file.
- **Response**: HDF5 file download.

### Import Orders from HDF5

- **URL**: `/orders/import/hdf5`
- **Method**: `POST`
- **Description**: Imports orders from an HDF5 file.
- **Request**: Upload HDF5 file.

- **Response**:

  ```json
  {
      "message": "Orders imported successfully"
  }
  ```

### Export Orders to XML

- **URL**: `/orders/export/xml`
- **Method**: `GET`
- **Description**: Exports orders to an XML file.
- **Response**: XML file download.

### Import Orders from XML

- **URL**: `/orders/import/xml`
- **Method**: `POST`
- **Description**: Imports orders from an XML file.
- **Request**: Upload XML file.

- **Response**:

  ```json
  {
      "message": "Orders imported successfully"
  }
  ```
  

## Running the Tests

**Run the tests**:

   ```bash
   pytest
   ```

## Sample Files

- **HDF5 File**: A sample HDF5 file can be found in the `samples` directory.
- **XML File**: A sample XML file can be found in the `samples` directory.
- **XLSX Report**: A sample XLSX report can be found in the `samples` directory.

## License

This project is licensed under the [MIT License](LICENSE).