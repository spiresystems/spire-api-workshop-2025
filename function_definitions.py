function_definitions = [
    {
        "name": "search_customers",
        "description": "Search for customers based on name or customer number.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {"type": "string"}
            },
            "required": ["search_query"]
        }
    }
    ,{
        "name": "get_latest_sales_orders",
        "description": "Retrieve latest sales orders for a specific customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_no": {"type": "string"}
            },
            "required": ["customer_no"]
        }
    }
    ,{
        "name": "create_sales_order",
        "description": "Create a new sales order for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_no": {"type": "string"}
            },
            "required": ["customer_no"]
        }
    }
##    ,{
##        "name": "add_item_to_sales_order",
##        "description": "Add an item to an existing sales order.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_id": {"type": "integer"},
##                "warehouse": {"type": "string"},
##                "part_no": {"type": "string"},
##                "quantity": {"type": "number"}
##            },
##            "required": ["order_id", "warehouse", "part_no", "quantity"]
##        }
##    }
##    ,{
##        "name": "delete_item_from_sales_order",
##        "description": "Remove an item from an existing sales order.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_id": {"type": "integer"},
##                "sales_order_item_id": {"type": "integer"}
##            },
##            "required": ["order_id", "sales_order_item_id"]
##        }
##    }
##    ,{
##        "name": "modify_sales_order_item_quantity",
##        "description": "Update the order or ship quantity for an item in a sales order.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_id": {"type": "integer"},
##                "sales_order_item_id": {"type": "integer"},
##                "order_quantity": {"type": "number"},
##                "ship_quantity": {"type": "number"}
##            },
##            "required": ["order_id", "sales_order_item_id"]
##        }
##    }
##    ,{
##        "name": "get_sales_order_id_from_order_no",
##        "description": "Get the internal sales order ID given a sales order number.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_no": {"type": "string"}
##            },
##            "required": ["order_no"]
##        }
##    }
##    ,{
##        "name": "invoice_sales_order",
##        "description": "Invoice an existing sales order.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_id": {"type": "integer"}
##            },
##            "required": ["order_id"]
##        }
##    }
##    ,{
##        "name": "get_sales_order_detailed_by_order_id",
##        "description": "Fetch full details of a sales order by ID.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "order_id": {"type": "integer"}
##            },
##            "required": ["order_id"]
##        }
##    }
##    ,{
##        "name": "search_products",
##        "description": "Search for inventory items using part number or description.",
##        "parameters": {
##            "type": "object",
##            "properties": {
##                "search_query": {"type": "string"}
##            },
##            "required": ["search_query"]
##        }
##    }
]

def get_function_names():
    return [f["name"] for f in function_definitions]

def get_function_schemas():
    return [
        {
            "type": "function",
            **f
        } for f in function_definitions
    ]
