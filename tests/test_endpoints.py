import json
import os
import h5py
import xml.etree.ElementTree as ET
from datetime import datetime
from src.database.models import Order
from src.routes.services import export_orders_to_hdf5, export_orders_to_xml


def test_add_order(client, session):
    response = client.post('/api/orders', data=json.dumps({
        "name": "Test Order",
        "description": "Test Description",
        "status": "New"
    }), content_type='application/json')

    assert response.status_code == 201
    assert response.json['name'] == "Test Order"


def test_get_orders(client, session):
    client.post('/api/orders', data=json.dumps({
        "name": "Another Test Order",
        "description": "Another Test Description",
        "status": "New"
    }), content_type='application/json')

    response = client.get('/api/orders')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_order(client, session):
    response = client.post('/api/orders', data=json.dumps({
        "name": "Order to Retrieve",
        "description": "Description",
        "status": "New"
    }), content_type='application/json')

    order_id = response.json['id']
    response = client.get(f'/api/orders/{order_id}')
    assert response.status_code == 200
    assert response.json['name'] == "Order to Retrieve"


def test_edit_order(client, session):
    response = client.post('/api/orders', data=json.dumps({
        "name": "Order to Edit",
        "description": "Description",
        "status": "New"
    }), content_type='application/json')

    order_id = response.json['id']
    response = client.put(f'/api/orders/{order_id}', data=json.dumps({
        "name": "Edited Order",
        "description": "Edited Description",
        "status": "In Progress"
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['name'] == "Edited Order"


def test_delete_order(client, session):
    response = client.post('/api/orders', data=json.dumps({
        "name": "Order to Delete",
        "description": "Description",
        "status": "New"
    }), content_type='application/json')

    order_id = response.json['id']
    response = client.delete(f'/api/orders/{order_id}')
    assert response.status_code == 200

    response = client.get(f'/api/orders/{order_id}')
    assert response.status_code == 404


def test_bulk_update_status(client, session):
    order_ids = []
    for i in range(3):
        response = client.post('/api/orders', data=json.dumps({
            "name": f"Order {i}",
            "description": f"Description {i}",
            "status": "New"
        }), content_type='application/json')
        order_ids.append(response.json['id'])

    response = client.put('/api/orders/update', data=json.dumps({
        "order_ids": order_ids,
        "status": "Completed"
    }), content_type='application/json')

    assert response.status_code == 200
    assert all(order['status'] == "Completed" for order in response.json['updated_orders'])


def test_get_order_statistics(client, session):
    client.post('/api/orders', data=json.dumps({
        "name": "Order 1",
        "description": "Description 1",
        "status": "New"
    }), content_type='application/json')
    client.post('/api/orders', data=json.dumps({
        "name": "Order 2",
        "description": "Description 2",
        "status": "In Progress"
    }), content_type='application/json')
    client.post('/api/orders', data=json.dumps({
        "name": "Order 3",
        "description": "Description 3",
        "status": "Completed"
    }), content_type='application/json')

    response = client.get('/api/orders/statistics')
    assert response.status_code == 200
    assert response.json['New'] == 1
    assert response.json['In Progress'] == 1
    assert response.json['Completed'] == 1


def test_generate_report_xlsx(client, session):
    client.post('/api/orders', data=json.dumps({
        "name": "Order for Report",
        "description": "Description",
        "status": "New"
    }), content_type='application/json')

    response = client.get('/api/orders/report')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_export_orders_to_hdf5(session):
    order = Order(name="Order 1", description="Description 1", status="New", creation_date=datetime.utcnow())
    session.add(order)
    session.commit()

    file_path = export_orders_to_hdf5()
    assert os.path.exists(file_path)
    os.remove(file_path)


def test_import_orders_from_hdf5(client, session, tmpdir):
    file_path = tmpdir.join("orders.hdf5")
    with h5py.File(file_path, 'w') as f:
        f.create_dataset("id", data=[1])
        f.create_dataset("name", data=[b"Test Order"])
        f.create_dataset("description", data=[b"Test Description"])
        f.create_dataset("status", data=[b"New"])
        f.create_dataset("creation_date", data=[str(datetime.utcnow()).encode()])

    with open(file_path, 'rb') as f:
        response = client.post('/api/orders/import/hdf5', data={'file': (f, "orders.hdf5")})
        assert response.status_code == 200
        assert response.json['message'] == "Orders imported successfully"

    response = client.get('/api/orders')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Test Order"


def test_export_orders_to_xml(session):
    order = Order(name="Order 1", description="Description 1", status="New", creation_date=datetime.utcnow())
    session.add(order)
    session.commit()

    file_path = export_orders_to_xml()
    assert os.path.exists(file_path)
    os.remove(file_path)


def test_import_orders_from_xml(client, session, tmpdir):
    file_path = tmpdir.join("orders.xml")
    root = ET.Element("orders")
    order_elem = ET.Element("order")
    ET.SubElement(order_elem, "id").text = "1"
    ET.SubElement(order_elem, "name").text = "Test Order"
    ET.SubElement(order_elem, "description").text = "Test Description"
    ET.SubElement(order_elem, "status").text = "New"
    ET.SubElement(order_elem, "creation_date").text = str(datetime.utcnow())
    root.append(order_elem)
    tree = ET.ElementTree(root)
    tree.write(file_path)

    with open(file_path, 'rb') as f:
        response = client.post('/api/orders/import/xml', data={'file': (f, "orders.xml")})
        assert response.status_code == 200
        assert response.json['message'] == "Orders imported successfully"

    response = client.get('/api/orders')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Test Order"
