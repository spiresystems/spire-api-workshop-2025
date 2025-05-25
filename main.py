from spire_client import get_latest_sales_orders, is_valid_connection, search_customers, create_sales_order 
from agent import agent_loop
from config import runtime_config

def prompt_credentials():
    print("Please enter your API connection credentials:")
    runtime_config["company"] = input("Company (database name): ").strip()
    runtime_config["username"] = input("Username: ").strip()
    runtime_config["password"] = input("Password: ").strip()

    if not is_valid_connection():
        prompt_credentials()

def list_sales_orders(args):
    customer_no = args[0] if args else None

    try:
        orders = get_latest_sales_orders(customer_no=customer_no)
        if not orders:
            print("No sales orders found.")
            return

        for order in orders:
            print(
                f"Order: {order['orderNo']} | "
                f"Customer: {order['customer']['name']} | "
                f"Status: {order['status']} | "
                f"Order Date: {order['orderDate']} | "
                f"Total: ${order['total']}"
            )
    except Exception as e:
        print(f"Error: {e}")

def customer_search(args):
    if not args:
        print("Usage: search-customers <search_term>")
        return 

    query = " ".join(args)
    try:
        customers = search_customers(query)
        if not customers:
            print("No customers found.")
            return

        for c in customers:
            print(f"{c['customerNo']} - {c['name']} (Credit: ${c['creditLimit']}, Open Orders: ${c['openOrders']})")
    except Exception as e:
        print(f"Error: {e}")


def create_order(args):
    if not args:
        print("Usage: create-order <customer_no>")
        return

    customer_no = args[0]

    try:
        result = create_sales_order(customer_no)
        if result.get("success"):
            print(f"{result['message']}")
            if result.get("order_id"):
                print(f"Order ID: {result['order_id']}")
        else:
            print(f"Failed to create sales order: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Error: {e}")



def cli_tool():
    print("Welcome to Spire CLI. Type 'help' to see available commands.\n")

    while True:
        command_line = input("> ").strip()
        if not command_line:
            continue

        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        if command == "exit":
            break
        elif command == "help":
            print("Commands:")
            print("  list-sales-orders [customer_no] - View latest sales orders")
##            print("  search-customers [search_term] - Search for customers by name or number") 
##            print("  create-order [customer_no] - Create an empty sales order for a customer") 
            print("  exit - Quit the program")
        elif command == "list-sales-orders":
            list_sales_orders(args)
        elif command == "search-customers":
            customer_search(args)
        elif command == "create-order":
            create_order(args)
        else:
            print(f"Unknown command: {command}. Type 'help' for a list.")

def chatgpt():
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        agent_loop(query)

if __name__ == "__main__":
    try:
        prompt_credentials()
        cli_tool()
##        chatgpt() 
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
