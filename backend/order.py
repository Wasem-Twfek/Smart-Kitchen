from typing import List, Dict, Any

class OrderManager:
    def __init__(self):
        self.orders = []  # List of order dicts

    def generate_order_list(self, missing_ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Accepts a list of missing ingredient dicts and returns the shopping list.
        """
        self.orders = missing_ingredients
        return self.orders

    def save_order_list(self, path: str = "order_list.txt"):
        """
        Saves the current order list to a text file.
        """
        with open(path, 'w', encoding='utf-8') as f:
            for item in self.orders:
                f.write(f"{item['name']}: {item['quantity']} {item['unit']}\n")

    def print_order_list(self):
        """
        Prints the current order list to the console.
        """
        if not self.orders:
            print("No items to order!")
            return
        print("Shopping List:")
        for item in self.orders:
            print(f"- {item['name']}: {item['quantity']} {item['unit']}") 