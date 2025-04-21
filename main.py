import datetime as dt
import models

def receive_shipment_cli():
    print("Welcome to the Shipment Management System")
    
    item_name = input("Enter the item name: ")
    item_id = input("Enter the item ID: ")
    item_quantity = input("Enter the item quantity: ")
    try:
        item_quantity = int(item_quantity)
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return
    
    dimensions = (0, 0, 0)
    storage_requirements = {}
    unique_object_name = f"{item_name}_{item_id}"

    item_object = models.Item(item_name, item_id, item_quantity, dimensions, storage_requirements)
    
    if 'items_dict' not in globals():
        global items_dict
        items_dict = {}

    items_dict[unique_object_name] = item_object

    bin_id = input("Enter the storage bin ID to receive the shipment: ")

    try:
        models.warehouse.receive_shipment(item_object, bin_id)
        print(f"Shipment for {item_name} successfully received and stored in bin {bin_id}.")
    except Exception as e:
        print(f"Error receiving shipment: {str(e)}")

def process_order_cli():
    print("Welcome to the Order Processing System")

    order_id = input("Enter the order ID: ")
    order_items = {}

    while True:
        item_id = input("Enter item ID (or type 'done' to finish): ")
        if item_id.lower() == 'done':
            break
        quantity = input(f"Enter quantity for item {item_id}: ")
        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue
        
        order_items[item_id] = quantity

    if not order_items:
        print("No items in the order. Order processing cancelled.")
        return

    order = models.Order(order_id, order_items)

    try:
        result = models.warehouse.fulfill_order(order)
        print("Order processed successfully.")
        print(f"Order ID: {order.order_id}")
        print("Items:")
        for item_id, quantity in order.items.items():
            print(f"  - {item_id}: {quantity}")
    except Exception as e:
        print("Order processed unsuccessfully.")
        print(f"Order processing failed: {str(e)}")

def generate_report_cli():
    print("Generating warehouse inventory report...\n")

    try:
        report = models.warehouse.generate_inventory_report()
        print(report)
    except Exception as e:
        print("Error generating report.")
        print(f"Details: {str(e)}")

def add_storage_bin_cli():
    print("Add a New Storage Bin")

    bin_id = input("Enter bin ID: ")
    while True:
        capacity_input = input("Enter bin capacity: ")
        try:
            capacity = int(capacity_input)
            break  # اگر ظرفیت صحیح بود، از حلقه خارج می‌شود
        except ValueError:
            print("Invalid capacity. Please enter a valid number.")
            return  # برگشت به منو در صورت وارد کردن مقدار غیر عددی
        
    cons_input = input("Enter environmental requirements (key1=value1,key2=value2,...): ")
    constraints = {}

    try:
        for pair in cons_input.split(','):
            if '=' in pair:
                key, value = pair.split('=')
                constraints[key.strip()] = value.strip()
    except Exception:
        print("Invalid format for environmental requirements. Skipping them.")
        constraints = {} 

    new_bin = models.StorageBin(bin_id, capacity, constraints=constraints)

    try:
        models.warehouse.add_storage_bin(new_bin)
    except Exception as e:
        print(f"Error adding storage bin: {str(e)}")

def add_supplier_cli():
    print("Add a New Supplier")
    name = input("Enter supplier name: ")
    contact_input = input("Enter contact details (e.g., phone=123, email=abc@example.com): ")
    contact_details = {}

    try:
        for pair in contact_input.split(','):
            if '=' in pair:
                key, value = pair.split('=')
                contact_details[key.strip()] = value.strip()
    except Exception:
        print("Invalid format for contact details. Skipping them.")
        contact_details = {}

    try:
        new_supplier = models.Supplier(name, contact_details)
        models.warehouse.add_supplier(new_supplier)
    except Exception as e:
        print(f"Failed to add supplier: {str(e)}")

def main():
    models.warehouse = models.Warehouse()

    default_bin = models.StorageBin("1BIN", 1000)
    models.warehouse.add_storage_bin(default_bin)

    menu = """
Warehouse Management CLI
-------------------------
1. Receive Shipment
2. Process Order
3. Generate Inventory Report
4. Add Storage Bin
5. Add Supplier
6. Exit
"""
    while True:
        print(menu)
        choice = input("Select an option (1-6): ")

        if choice == "1":
            receive_shipment_cli()
        elif choice == "2":
            process_order_cli()
        elif choice == "3":
            generate_report_cli()
        elif choice == "4":
            add_storage_bin_cli()
        elif choice == "5":
            add_supplier_cli()
        elif choice == "6":
            print("Exiting the CLI. Goodbye!")
            break
        else:
            print("Invalid option. Please select a valid choice (1-6).")
