import os
import requests
import json
from requests.auth import HTTPBasicAuth
from config import runtime_config

def get_company(): return runtime_config["company"]
def get_username(): return runtime_config["username"]
def get_password(): return runtime_config["password"]
def get_base_url(): return runtime_config.get("base_url", "http://localhost:10880")

def is_valid_connection():
    url = f"{get_base_url()}/api/v2/companies/{get_company()}"
    headers = { "Accept": "application/json" }

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))

    if response.status_code == 200:
        return True
    else:
        return False

def get_latest_sales_orders(customer_no=None, start=0, limit=50):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/"
    headers = { "Accept": "application/json" }

    params = {
        "start": start,
        "limit": limit,
        "sort": "-id"
    }

    if customer_no:
        params["filter"] = json.dumps({ "customer.customerNo": customer_no })

    response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(get_username(), get_password()))

    if response.status_code == 200:
        return response.json().get("records", [])
    else:
        raise Exception(f"Failed to fetch sales orders. Status: {response.status_code} - {response.text}")


def search_customers(search_query):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/customers/"
    params = { "q": search_query }
    headers = { "Accept": "application/json" }

    response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(get_username(), get_password()))

    if response.status_code == 200:
        return response.json().get("records", [])
    else:
        raise Exception(f"Failed to search customers. Status: {response.status_code} - {response.text}")


def create_sales_order(customer_no):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "customer": { "customerNo": customer_no }
    }

    response = requests.post(url, headers=headers, json=payload, auth=HTTPBasicAuth(get_username(), get_password()))

    if response.status_code in [200, 201]:
        location = response.headers.get("Location")
        order_id = location.rstrip("/").split("/")[-1] if location else None
        return {
            "success": True,
            "message": "Sales order created successfully.",
            "order_id": order_id,
            "location": location
        }
    else:
        raise Exception(f"Failed to create sales order. Status: {response.status_code} - {response.text}")


def get_sales_order_id_from_order_no(order_no):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/"
    headers = { "Accept": "application/json" }
    params = { "filter": json.dumps({ "orderNo": order_no }) }

    response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(get_username(), get_password()))
    if response.status_code == 200:
        records = response.json().get("records", [])
        if not records:
            raise Exception(f"No sales order found for order number {order_no}")
        return records[0]["id"]
    else:
        raise Exception(f"Failed to look up order ID. Status: {response.status_code} - {response.text}")


def get_sales_order_detailed_by_order_id(order_id):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    headers = { "Accept": "application/json" }

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch order details. Status: {response.status_code} - {response.text}")


def search_products(search_query):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/inventory/items/"
    params = { "q": search_query }
    headers = { "Accept": "application/json" }

    response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(get_username(), get_password()))
    if response.status_code == 200:
        return response.json().get("records", [])
    else:
        raise Exception(f"Failed to search products. Status: {response.status_code} - {response.text}")
    

def add_item_to_sales_order(order_id, warehouse, part_no, quantity):
    get_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    headers = { "Accept": "application/json", "Content-Type": "application/json" }

    get_response = requests.get(get_url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))
    if get_response.status_code != 200:
        raise Exception(f"Failed to fetch order. Status: {get_response.status_code} - {get_response.text}")

    existing_items = get_response.json().get("items", [])
    item_id_entries = [{"id": item["id"]} for item in existing_items if "id" in item]
    new_item = { "whse": warehouse, "partNo": part_no, "orderQty": str(quantity) }
    updated_items = item_id_entries + [new_item]

    put_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    payload = { "items": updated_items }

    put_response = requests.put(put_url, headers=headers, json=payload, auth=HTTPBasicAuth(get_username(), get_password()))
    if put_response.status_code in [200, 204]:
        return { "success": True, "message": "Item added successfully" }
    else:
        raise Exception(f"Failed to update order. Status: {put_response.status_code} - {put_response.text}")


def delete_item_from_sales_order(order_id, sales_order_item_id):
    get_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    headers = { "Accept": "application/json", "Content-Type": "application/json" }

    get_response = requests.get(get_url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))
    if get_response.status_code != 200:
        raise Exception(f"Failed to fetch order. Status: {get_response.status_code} - {get_response.text}")

    existing_items = get_response.json().get("items", [])
    updated_items = [{"id": item["id"]} for item in existing_items if item.get("id") != sales_order_item_id]

    put_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    payload = { "items": updated_items }

    put_response = requests.put(put_url, headers=headers, json=payload, auth=HTTPBasicAuth(get_username(), get_password()))
    if put_response.status_code in [200, 204]:
        return { "success": True, "message": f"Item {sales_order_item_id} removed from order {order_id}." }
    else:
        raise Exception(f"Failed to update order. Status: {put_response.status_code} - {put_response.text}")


def modify_sales_order_item_quantity(order_id, sales_order_item_id, order_quantity=None, ship_quantity=None):
    get_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    headers = { "Accept": "application/json", "Content-Type": "application/json" }

    get_response = requests.get(get_url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))
    if get_response.status_code != 200:
        raise Exception(f"Failed to fetch order. Status: {get_response.status_code} - {get_response.text}")

    items = get_response.json().get("items", [])
    updated_items = []
    found = False

    for item in items:
        if item.get("id") == sales_order_item_id:
            updated_item = { "id": item["id"] }
            if order_quantity is not None:
                updated_item["orderQty"] = str(order_quantity)
            if ship_quantity is not None:
                updated_item["committedQty"] = str(ship_quantity)
            updated_items.append(updated_item)
            found = True
        else:
            updated_items.append({ "id": item["id"] })

    if not found:
        raise Exception(f"Item ID {sales_order_item_id} not found in order {order_id}.")

    put_url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}"
    payload = { "items": updated_items }

    put_response = requests.put(put_url, headers=headers, json=payload, auth=HTTPBasicAuth(get_username(), get_password()))
    if put_response.status_code in [200, 204]:
        return { "success": True, "message": f"Item {sales_order_item_id} updated in order {order_id}." }
    else:
        raise Exception(f"Failed to update quantity. Status: {put_response.status_code} - {put_response.text}")


def invoice_sales_order(order_id):
    url = f"{get_base_url()}/api/v2/companies/{get_company()}/sales/orders/{order_id}/invoice"
    headers = { "Accept": "application/json" }

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(get_username(), get_password()))
    if response.status_code in [200, 201, 204]:
        return { "success": True, "message": f"Sales order {order_id} invoiced successfully." }
    else:
        raise Exception(f"Failed to invoice order. Status: {response.status_code} - {response.text}")


