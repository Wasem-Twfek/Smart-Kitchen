import json
from typing import List, Dict, Any
from datetime import datetime
from pint import UnitRegistry
import os

ureg = UnitRegistry()

def normalize_unit(quantity, unit):
    try:
        q = ureg(f"{quantity} {unit}")
        if q.check('[volume]'):
            return float(q.to('milliliter').magnitude), 'ml'
        elif q.check('[mass]'):
            return float(q.to('gram').magnitude), 'g'
        else:
            return float(quantity), unit
    except Exception:
        return float(quantity), unit

class Fridge:
    def __init__(self, owner: str, fridge_id: str, items: List[Dict[str, Any]]):
        self.owner = owner
        self.fridge_id = fridge_id
        self.items = items  # List of dicts: name, quantity, unit, perishable, expiry_date (optional)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Fridge(
            owner=data["owner"],
            fridge_id=data["fridge_id"],
            items=data["items"]
        )

def filter_expired_items(items: List[Dict[str, Any]]):
    today = datetime.today().date()
    valid_items = []
    expired_items = []
    for item in items:
        expiry = item.get('expiry_date')
        if expiry:
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                if expiry_date < today:
                    expired_items.append(item)
                else:
                    valid_items.append(item)
            except Exception:
                valid_items.append(item)
        else:
            valid_items.append(item)
    return valid_items, expired_items

class FridgeManager:
    def __init__(self, fridges=None):
        # Initialize fridges as a dictionary
        self.fridges = {}
        
        if fridges is not None:
            # Handle different input formats
            if isinstance(fridges, list):
                # If fridges is a list of Fridge objects from old format
                for fridge in fridges:
                    if isinstance(fridge, dict) and 'fridge_id' in fridge and 'items' in fridge:
                        self.fridges[fridge['fridge_id']] = fridge['items']
                    elif hasattr(fridge, 'fridge_id') and hasattr(fridge, 'items'):
                        self.fridges[fridge.fridge_id] = fridge.items
            elif isinstance(fridges, dict):
                # If fridges is already a dictionary
                self.fridges = fridges

    @classmethod
    def load_from_json(cls, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert old format to new format if needed
            if isinstance(data, list):
                fridges_dict = {}
                for fridge in data:
                    if isinstance(fridge, dict) and 'fridge_id' in fridge and 'items' in fridge:
                        fridges_dict[fridge['fridge_id']] = fridge['items']
                return cls(fridges_dict)
            return cls(data)
        except FileNotFoundError:
            # If file doesn't exist, create an empty fridge manager
            return cls()
        except json.JSONDecodeError:
            # If file is not valid JSON, create an empty fridge manager
            return cls()

    def save_to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.fridges, f, indent=2)

    def get_fridge_ids(self):
        return list(self.fridges.keys())

    def get_fridge(self, fridge_id):
        return self.fridges.get(fridge_id, [])

    def add_item_to_fridge(self, fridge_id, item):
        if fridge_id not in self.fridges:
            self.fridges[fridge_id] = []
        
        # Check if item already exists
        existing_items = [i for i in self.fridges[fridge_id] if i['name'] == item['name'] and i.get('unit', '') == item.get('unit', '')]
        
        if existing_items:
            # Update existing item
            existing_items[0]['quantity'] += item['quantity']
            # Update expiry date if provided
            if 'expiry_date' in item and item['expiry_date']:
                existing_items[0]['expiry_date'] = item['expiry_date']
        else:
            # Add new item
            self.fridges[fridge_id].append(item)

    def remove_item(self, fridge_id, item_name):
        if fridge_id not in self.fridges:
            return
        
        self.fridges[fridge_id] = [i for i in self.fridges[fridge_id] if i['name'] != item_name]

    def consume_item(self, fridge_id, item_name, quantity=1):
        if fridge_id not in self.fridges:
            return
        
        for item in self.fridges[fridge_id]:
            if item['name'] == item_name:
                item['quantity'] = max(0, item['quantity'] - quantity)
                # Remove item if quantity becomes 0
                if item['quantity'] == 0:
                    self.remove_item(fridge_id, item_name)
                return

    def restock_item(self, fridge_id, item_name, quantity=1):
        if fridge_id not in self.fridges:
            return
        
        for item in self.fridges[fridge_id]:
            if item['name'] == item_name:
                item['quantity'] += quantity
                return

    def check_expired_items(self, fridge_id=None):
        expired_items = []
        today = datetime.now().date()
        
        if fridge_id:
            fridge_ids = [fridge_id]
        else:
            fridge_ids = self.get_fridge_ids()
            
        for fid in fridge_ids:
            for item in self.get_fridge(fid):
                if 'expiry_date' in item:
                    try:
                        expiry_date = datetime.strptime(item['expiry_date'], '%Y-%m-%d').date()
                        if expiry_date < today:
                            expired_items.append({
                                'fridge_id': fid,
                                'name': item['name'],
                                'quantity': item['quantity'],
                                'unit': item.get('unit', ''),
                                'expiry_date': item['expiry_date']
                            })
                    except (ValueError, TypeError):
                        # Invalid date format, skip
                        pass
                        
        return expired_items

    def combine_inventories(self, fridge_ids):
        combined_inventory = []
        expired_items = []
        
        for fridge_id in fridge_ids:
            if fridge_id not in self.fridges:
                continue
                
            for item in self.fridges[fridge_id]:
                # Check if item is expired
                is_expired = False
                if 'expiry_date' in item:
                    try:
                        expiry_date = datetime.strptime(item['expiry_date'], '%Y-%m-%d').date()
                        if expiry_date < datetime.now().date():
                            is_expired = True
                            expired_item = item.copy()
                            expired_item['fridge_id'] = fridge_id
                            expired_items.append(expired_item)
                    except (ValueError, TypeError):
                        # Invalid date format, treat as not expired
                        pass
                
                if not is_expired:
                    # Check if item exists in combined inventory
                    existing_items = [i for i in combined_inventory if i['name'] == item['name'] and i.get('unit', '') == item.get('unit', '')]
                    
                    if existing_items:
                        # Update existing item
                        existing_items[0]['quantity'] += item['quantity']
                    else:
                        # Add new item
                        combined_inventory.append(item.copy())
        
        return combined_inventory, expired_items

    def list_perishables(self, inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in inventory if item.get("perishable", False)]

    def list_non_perishables(self, inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in inventory if not item.get("perishable", True)] 