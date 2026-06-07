import os
from backend.fridge import FridgeManager
from backend.planner import RecipePlanner, RECIPES
from backend.order import OrderManager
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime

def load_utensils(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [item['name'] for item in data]

def load_structured_recipes(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

app = Flask(__name__)
app.secret_key = 'smartkitchen-secret'  # Needed for flash messages
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    fridge_path = os.path.join('data', 'fridges.json')
    utensils_path = os.path.join('data', 'kitchenware.json')
    structured_path = os.path.join('data', 'structured_recipes.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    utensils = load_utensils(utensils_path)
    fridge_ids = fridge_manager.get_fridge_ids()
    structured_recipes = load_structured_recipes(structured_path)
    result = None
    selected_fridges = []
    servings = ''
    recipe_details = None
    expired_items = []
    show_results = False
    if request.method == 'POST':
        selected_fridges = request.form.getlist('fridges')
        servings = request.form.get('servings', '')
        action = request.form.get('action', 'recommend')
        try:
            servings_int = int(servings)
            inventory, expired_items = fridge_manager.combine_inventories(selected_fridges)
            planner = RecipePlanner(RECIPES)
            result = planner.recommend(inventory, utensils, servings_int)
            show_results = True
            # Find details in structured_recipes.json if available
            if result['recipe']:
                for r in structured_recipes:
                    if r['title'].lower() == result['recipe']['name'].lower():
                        recipe_details = r
                        break
            # Save order if requested
            if action == 'save_order' and result['missing_ingredients']:
                order_mgr = OrderManager()
                order_mgr.generate_order_list(result['missing_ingredients'])
                order_mgr.save_order_list()
                flash('Shopping list saved to order_list.txt!', 'success')
                show_results = True
            # Simulate a fridge update event for real-time sync
            socketio.emit('fridge_updated', {'fridges': selected_fridges})
        except Exception as e:
            result = {'error': str(e)}
    return render_template('index.html', 
                          fridge_ids=fridge_ids, 
                          selected_fridges=selected_fridges, 
                          servings=servings, 
                          result=result, 
                          recipe_details=recipe_details, 
                          expired_items=expired_items, 
                          show_results=show_results)

@app.route('/inventory')
def inventory():
    fridge_path = os.path.join('data', 'fridges.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    fridges = []
    
    # Format fridges for template
    for fridge_id in fridge_manager.get_fridge_ids():
        fridge_data = fridge_manager.get_fridge(fridge_id)
        inventory = []
        
        # Format inventory items
        for item in fridge_data:
            # Check if item is expired
            is_expired = False
            if 'expiry_date' in item:
                try:
                    expiry_date = datetime.strptime(item['expiry_date'], '%Y-%m-%d')
                    is_expired = expiry_date < datetime.now()
                except:
                    pass
            
            inventory.append({
                'name': item['name'],
                'quantity': item['quantity'],
                'unit': item['unit'],
                'expiry_date': item.get('expiry_date', ''),
                'is_expired': is_expired
            })
        
        fridges.append({
            'id': fridge_id,
            'inventory': inventory
        })
    
    return render_template('inventory.html', fridges=fridges)

@app.route('/recipes')
def recipes():
    structured_path = os.path.join('data', 'structured_recipes.json')
    recipe_list = []
    
    # Load structured recipes
    structured_recipes = load_structured_recipes(structured_path)
    for idx, recipe in enumerate(RECIPES):
        recipe_data = {
            'id': idx,
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'utensils': recipe.get('utensils', []),
            'tags': ['vegetarian'] if any('vegetarian' in r.get('tags', []) for r in structured_recipes if r['title'].lower() == recipe['name'].lower()) else [],
            'image': None
        }
        
        # Find additional data from structured recipes
        for r in structured_recipes:
            if r['title'].lower() == recipe['name'].lower():
                recipe_data['description'] = r.get('description', '')
                if 'steps' in r:
                    recipe_data['steps'] = r['steps']
                if 'tags' in r:
                    recipe_data['tags'] = r['tags']
                break
        
        recipe_list.append(recipe_data)
    
    return render_template('recipes.html', recipes=recipe_list)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    if recipe_id < 0 or recipe_id >= len(RECIPES):
        flash('Recipe not found', 'error')
        return redirect(url_for('recipes'))
    
    recipe = RECIPES[recipe_id]
    structured_path = os.path.join('data', 'structured_recipes.json')
    structured_recipes = load_structured_recipes(structured_path)
    
    recipe_data = {
        'id': recipe_id,
        'name': recipe['name'],
        'ingredients': recipe['ingredients'],
        'utensils': recipe.get('utensils', []),
        'steps': [],
        'tags': []
    }
    
    # Find additional data from structured recipes
    for r in structured_recipes:
        if r['title'].lower() == recipe['name'].lower():
            recipe_data['description'] = r.get('description', '')
            if 'steps' in r:
                recipe_data['steps'] = r['steps']
            if 'if_then_rules' in r:
                recipe_data['if_then_rules'] = r['if_then_rules']
            if 'tags' in r:
                recipe_data['tags'] = r['tags']
            break
    
    return render_template('recipe_details.html', recipe=recipe_data)

@app.route('/check_ingredients/<int:recipe_id>')
def check_ingredients(recipe_id):
    # This is a stub - would be integrated with actual inventory management
    if recipe_id < 0 or recipe_id >= len(RECIPES):
        return jsonify({'success': False, 'message': 'Recipe not found'})
    
    # Simulate checking ingredients
    recipe = RECIPES[recipe_id]
    
    # For demo: randomly mark some ingredients as missing
    import random
    missing = []
    if recipe['ingredients']:
        missing_count = random.randint(0, min(3, len(recipe['ingredients'])))
        missing = [ing['name'] for ing in random.sample(recipe['ingredients'], missing_count)]
    
    return jsonify({
        'success': True, 
        'missing': missing,
        'message': 'Ingredients checked successfully'
    })

@app.route('/add_item', methods=['POST'])
def add_item():
    fridge_id = request.form.get('fridge_id')
    item_name = request.form.get('item_name')
    quantity = float(request.form.get('quantity', 0))
    unit = request.form.get('unit')
    expiry_date = request.form.get('expiry_date', '')
    
    if not all([fridge_id, item_name, quantity, unit]):
        flash('Missing required fields', 'error')
        return redirect(url_for('inventory'))
    
    # Load fridges data
    fridge_path = os.path.join('data', 'fridges.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    
    # Add item to fridge
    try:
        item_data = {
            'name': item_name,
            'quantity': quantity,
            'unit': unit
        }
        if expiry_date:
            item_data['expiry_date'] = expiry_date
            
        fridge_manager.add_item_to_fridge(fridge_id, item_data)
        fridge_manager.save_to_json(fridge_path)
        
        flash(f'Added {item_name} to {fridge_id}', 'success')
    except Exception as e:
        flash(f'Error adding item: {str(e)}', 'error')
    
    return redirect(url_for('inventory'))

@app.route('/update_item', methods=['POST'])
def update_item():
    data = request.get_json()
    fridge_id = data.get('fridge_id')
    item_name = data.get('item_name')
    action = data.get('action')
    
    if not all([fridge_id, item_name, action]):
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Load fridges data
    fridge_path = os.path.join('data', 'fridges.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    
    # Update item in fridge
    try:
        if action == 'consume':
            # Simulate consumption (reduce quantity by 1 unit)
            fridge_manager.consume_item(fridge_id, item_name, 1)
        elif action == 'restock':
            # Simulate restocking (increase quantity by 1 unit)
            fridge_manager.restock_item(fridge_id, item_name, 1)
            
        fridge_manager.save_to_json(fridge_path)
        
        return jsonify({
            'success': True, 
            'message': f'Successfully updated {item_name} in {fridge_id}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.get_json()
    fridge_id = data.get('fridge_id')
    item_name = data.get('item_name')
    
    if not all([fridge_id, item_name]):
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Load fridges data
    fridge_path = os.path.join('data', 'fridges.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    
    # Delete item from fridge
    try:
        fridge_manager.remove_item(fridge_id, item_name)
        fridge_manager.save_to_json(fridge_path)
        
        return jsonify({
            'success': True, 
            'message': f'Successfully deleted {item_name} from {fridge_id}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@socketio.on('update_fridge')
def handle_update(data):
    emit('fridge_updated', data, broadcast=True)

# CLI improvements
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    COLORAMA = True
except ImportError:
    COLORAMA = False

def cprint(msg, color=None):
    if COLORAMA and color:
        print(color + msg + Style.RESET_ALL)
    else:
        print(msg)

def main():
    # Load fridges and utensils
    fridge_path = os.path.join('data', 'fridges.json')
    utensils_path = os.path.join('data', 'kitchenware.json')
    structured_path = os.path.join('data', 'structured_recipes.json')
    fridge_manager = FridgeManager.load_from_json(fridge_path)
    utensils = load_utensils(utensils_path)
    structured_recipes = load_structured_recipes(structured_path)

    print("Available fridges:")
    for idx, fridge_id in enumerate(fridge_manager.get_fridge_ids()):
        print(f"  {idx+1}. {fridge_id}")
    selected = input("Select fridges by number (comma-separated, e.g. 1,2): ")
    selected_ids = [fridge_manager.get_fridge_ids()[int(i.strip())-1] for i in selected.split(',') if i.strip().isdigit()]

    while True:
        try:
            servings = int(input("Enter number of servings: "))
            break
        except ValueError:
            cprint("Please enter a valid number for servings.", Fore.YELLOW if COLORAMA else None)
    inventory, expired_items = fridge_manager.combine_inventories(selected_ids)
    if expired_items:
        cprint("\nWarning: The following items are expired and were excluded from planning:", Fore.YELLOW if COLORAMA else None)
        for item in expired_items:
            cprint(f"  - {item['name']} ({item['quantity']} {item['unit']}, expired {item['expiry_date']})", Fore.YELLOW if COLORAMA else None)
    planner = RecipePlanner(RECIPES)
    result = planner.recommend(inventory, utensils, servings)
    recipe = result['recipe']
    missing_ingredients = result['missing_ingredients']
    missing_utensils = result['missing_utensils']

    recipe_details = None
    if recipe:
        for r in structured_recipes:
            if r['title'].lower() == recipe['name'].lower():
                recipe_details = r
                break
        cprint(f"\nRecommended recipe: {recipe['name']}", Fore.GREEN if COLORAMA else None)
        print("Ingredients:")
        for ing in recipe['ingredients']:
            found = not any(miss['name'] == ing['name'] and miss['unit'] == ing['unit'] for miss in missing_ingredients)
            color = Fore.GREEN if found and COLORAMA else (Fore.RED if COLORAMA else None)
            cprint(f"  - {ing['name']}: {ing['quantity']} {ing['unit']}", color)
        print("Utensils:")
        for u in recipe['utensils']:
            print(f"  - {u}")
        if missing_ingredients or missing_utensils:
            cprint("\nMissing items:", Fore.YELLOW if COLORAMA else None)
            if missing_ingredients:
                print("  Ingredients:")
                for item in missing_ingredients:
                    cprint(f"    - {item['name']}: {item['quantity']} {item['unit']}", Fore.RED if COLORAMA else None)
            if missing_utensils:
                print("  Utensils:")
                for u in missing_utensils:
                    cprint(f"    - {u}", Fore.RED if COLORAMA else None)
            order_mgr = OrderManager()
            order_mgr.generate_order_list(missing_ingredients)
            action = input("\nWould you like to save the shopping list to a file (s), print it (p), or skip (enter)? ").strip().lower()
            if action == 's':
                order_mgr.save_order_list()
                cprint("Shopping list saved to order_list.txt.", Fore.GREEN if COLORAMA else None)
            elif action == 'p':
                order_mgr.print_order_list()
        if recipe_details:
            print("\nRecipe Steps:")
            for step in recipe_details.get('steps', []):
                print(f"  - {step}")
            if recipe_details.get('if_then_rules'):
                print("IF–THEN Rules:")
                for rule in recipe_details['if_then_rules']:
                    print(f"  If {rule['if']}, then {rule['then']}")
            if recipe_details.get('ingredients'):
                print("Detected Ingredients:", ', '.join(recipe_details['ingredients']))
            if recipe_details.get('actions'):
                print("Detected Actions:", ', '.join(recipe_details['actions']))
            if recipe_details.get('contradictions'):
                cprint("Contradictions detected in recipe:", Fore.YELLOW if COLORAMA else None)
                for c in recipe_details['contradictions']:
                    cprint(f"  - {c}", Fore.YELLOW if COLORAMA else None)
    else:
        cprint("No suitable recipe found for the selected fridges and servings.", Fore.RED if COLORAMA else None)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        socketio.run(app, debug=True)
    else:
        main() 