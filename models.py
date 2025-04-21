class Item:
    def __init__(self, name, SKU, quantity=0, dimensions=(0, 0, 0), storage_requirements=None):
        self.name = name
        self.SKU = SKU
        self.quantity = int(quantity)
        self.dimensions = dimensions
        self.storage_requirements = storage_requirements if storage_requirements else {}

    def update_quantity(self, quantity):
        new_quantity = self.quantity + int(quantity)
        if new_quantity < 0:
            raise ValueError("quantity cannot be negative")
        self.quantity = new_quantity
    
    def display_info(self):
        return (
            f"Item Info:\n"
            f"Name: {self.name}\n"
            f"SKU: {self.SKU}\n"
            f"quantity: {self.quantity}\n"
            f"Dimensions: {self.dimensions}\n"
            f"Storage Requirements: {self.storage_requirements}"
        )

class StorageBin:
    def __init__(self, bin_id, capacity, current_load=0, constraints=None):
        self.bin_id = bin_id
        self.capacity = int(capacity)
        self.current_load = int(current_load)
        self.constraints = constraints if constraints else {}
        self.items = {}

    def add_item(self, item):
        if not isinstance(item, Item):
            raise TypeError("Only instances of Item can be added to the bin.")
        
        # Check storage requirements
        for req, value in item.storage_requirements.items():
            if req in self.constraints and self.constraints[req] != value:
                raise ValueError(f"Item does not meet bin's {req} requirement")
        
        required_space = item.quantity
        if self.current_load + required_space > self.capacity:
            raise ValueError("Not enough space in the bin")
        
        if item.SKU in self.items:
            self.items[item.SKU]['quantity'] += item.quantity
        else:
            self.items[item.SKU] = {
                'quantity': item.quantity,
                'name': item.name,
                'dimensions': item.dimensions
            }
        
        self.current_load += required_space

    def remove_item(self, item):
        if not isinstance(item, Item):
            raise TypeError("Only instances of Item can be removed from the bin.")
        
        if item.SKU not in self.items:
            raise ValueError("Item not found in the bin")
        
        if self.items[item.SKU]['quantity'] < item.quantity:
            raise ValueError("Not enough items in the bin to remove")
        
        self.items[item.SKU]['quantity'] -= item.quantity
        self.current_load -= item.quantity

        if self.items[item.SKU]['quantity'] == 0:
            del self.items[item.SKU]

    def available_space(self):
        return self.capacity - self.current_load
    
    def display_bin_info(self):
        info = (
            f"Bin Info:\n"
            f"Bin ID: {self.bin_id}\n"
            f"Capacity: {self.capacity}\n"
            f"Current Load: {self.current_load}\n"
            f"Available Space: {self.available_space()}\n"
            f"Constraints: {self.constraints}\n"
            f"Items in Bin:\n"
        )
        
        for sku, details in self.items.items():
            info += (
                f"  - SKU: {sku}, Name: {details['name']}, "
                f"quantity: {details['quantity']}, Dimensions: {details['dimensions']}\n"
            )
        
        return info


from datetime import datetime

class Order:
    def __init__(self, order_id: str, items: dict):
        self.order_id = order_id
        self.items = items  # Dictionary with SKU as key and quantity as value
        self.order_date = datetime.now()
        self.order_status = "Pending"  # Default status
    
    def process_order(self, warehouse):
        """
        Processes the order by checking inventory and updating status
        Returns True if successful, False otherwise
        """
        # Check if all items are available in inventory
        for sku, quantity in self.items.items():
            if sku not in warehouse.inventory or warehouse.inventory[sku].quantity < quantity:
                raise ValueError(f"Not enough inventory for item with SKU {sku}")
        
        # If all items are available, process the order
        try:
            for sku, quantity in self.items.items():
                # Create a temporary item for removal
                temp_item = Item("", sku, quantity)
                warehouse.remove_item_from_bins(temp_item)
                warehouse.inventory[sku].update_quantity(-quantity)
            
            self.update_status("Fulfilled")
            return True
        except Exception as e:
            raise RuntimeError(f"Error processing order: {str(e)}")
    
    def update_status(self, new_status: str):
        """
        Updates the order status
        Valid statuses: Pending, Fulfilled
        """
        valid_statuses = ["Pending", "Fulfilled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.order_status = new_status
    
    def display_order_info(self):
        """
        Returns formatted string with order details
        """
        items_info = "\n".join([f"  - SKU: {sku}, quantity: {qty}" for sku, qty in self.items.items()])
        return (
            f"Order Info:\n"
            f"Order ID: {self.order_id}\n"
            f"Order Date: {self.order_date}\n"
            f"Status: {self.order_status}\n"
            f"Items:\n{items_info}"
        )
class Supplier:
    def __init__(self, supplier_name, contact_details, items_supplied=None):
        self.supplier_name = supplier_name
        self.contact_details = contact_details
        self.items_supplied = items_supplied if items_supplied is not None else []
    
    def place_order(self):
        print(f"Order placed with supplier: {self.supplier_name}")
    
    def update_contact(self, new_contact_details):
        self.contact_details = new_contact_details
        print(f"Contact details updated for supplier: {self.supplier_name}")
    
    def display_supplier_info(self):
        return (
            f"Supplier Info:\n"
            f"Name: {self.supplier_name}\n"
            f"Contact Details: {self.contact_details}\n"
            f"Items Supplied: {', '.join(self.items_supplied) if self.items_supplied else 'None'}"
        )

class Warehouse:
    def __init__(self):
        self.storage_bins = {}
        self.inventory = {}
        self.orders = []
        self.suppliers = []
    
    def add_storage_bin(self, storage_bin):
        if not isinstance(storage_bin, StorageBin):
            raise TypeError("Only instances of StorageBin can be added to warehouse.")
        if storage_bin.bin_id in self.storage_bins:
            raise ValueError(f"Storage bin with ID {storage_bin.bin_id} already exists.")
        self.storage_bins[storage_bin.bin_id] = storage_bin
        print(f"Storage bin {storage_bin.bin_id} added successfully.")
    
    def add_supplier(self, supplier):
        if not isinstance(supplier, Supplier):
            raise TypeError("Only instances of Supplier can be added to warehouse.")
        self.suppliers.append(supplier)
        print(f"Supplier {supplier.supplier_name} added successfully.")
    
    def receive_shipment(self, item, bin_id):
        if not isinstance(item, Item):
            raise TypeError("Only instances of Item can be received.")
        
        if bin_id not in self.storage_bins:
            raise ValueError(f"Storage bin {bin_id} not found.")
        
        storage_bin = self.storage_bins[bin_id]
        
        try:
            storage_bin.add_item(item)
            
            # Update inventory
            if item.SKU in self.inventory:
                self.inventory[item.SKU].update_quantity(item.quantity)
            else:
                self.inventory[item.SKU] = item
            
            print(f"Shipment received and added to bin {bin_id} successfully.")
        except Exception as e:
            print(f"Error receiving shipment: {str(e)}")
    
    def fulfill_order(self, order):
        if not isinstance(order, Order):
            raise TypeError("Only instances of Order can be processed.")
        
        # Check inventory for all items
        for sku, quantity in order.items.items():
            if sku not in self.inventory or self.inventory[sku].quantity < quantity:
                print(f"Not enough inventory for item with SKU {sku}")
                return False
        
        # Process the order
        try:
            for sku, quantity in order.items.items():
                item_to_remove = Item("", sku, quantity)
                self.remove_item_from_bins(item_to_remove)
                self.inventory[sku].update_quantity(-quantity)
            
            order.update_status("Fulfilled")
            self.orders.append(order)
            print("Order fulfilled successfully.")
            return True
        except Exception as e:
            print(f"Error fulfilling order: {str(e)}")
            return False
    
    def generate_inventory_report(self):
        report = "Inventory Report:\n\n"
        
        # Inventory summary
        report += "Inventory Summary:\n"
        for sku, item in self.inventory.items():
            report += f"  - SKU: {sku}, Name: {item.name}, quantity: {item.quantity}\n"
        # Storage bins status
        report += "\nStorage Bins Status:\n"
        for bin_id, storage_bin in self.storage_bins.items():
            report += f"  - Bin ID: {bin_id}, Capacity: {storage_bin.capacity}, "
            report += f"Current Load: {storage_bin.current_load}, "
            report += f"Available Space: {storage_bin.available_space()}\n"
        
        return report
    
    def find_item(self, sku):
        return self.inventory.get(sku, None)
    
    def remove_item_from_bins(self, item):
        if not isinstance(item, Item):
            raise TypeError("Only instances of Item can be removed.")
        
        remaining_quantity = item.quantity
        
        for bin_id, storage_bin in self.storage_bins.items():
            if remaining_quantity <= 0:
                break
            
            if item.SKU in storage_bin.items:
                available_quantity = storage_bin.items[item.SKU]['quantity']
                quantity_to_remove = min(available_quantity, remaining_quantity)
                
                temp_item = Item("", item.SKU, quantity_to_remove)
                storage_bin.remove_item(temp_item)
                remaining_quantity -= quantity_to_remove
        
        if remaining_quantity > 0:
            raise ValueError(f"Could not remove all items. {remaining_quantity} items not found in bins.")