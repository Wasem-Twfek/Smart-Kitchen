import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kitchen.db')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Fridges table
    c.execute('''
        CREATE TABLE IF NOT EXISTS fridges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT,
            fridge_id TEXT,
            items TEXT -- JSON string
        )
    ''')
    # Utensils table
    c.execute('''
        CREATE TABLE IF NOT EXISTS utensils (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER
        )
    ''')
    # Recipes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            ingredients TEXT, -- JSON string
            utensils TEXT,    -- JSON string
            servings INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_fridge(owner, fridge_id, items, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO fridges (owner, fridge_id, items) VALUES (?, ?, ?)',
              (owner, fridge_id, json.dumps(items)))
    conn.commit()
    conn.close()

def fetch_fridges(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT owner, fridge_id, items FROM fridges')
    rows = c.fetchall()
    conn.close()
    return [
        {
            'owner': row[0],
            'fridge_id': row[1],
            'items': json.loads(row[2])
        } for row in rows
    ]

def insert_utensil(name, quantity, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO utensils (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()

def fetch_utensils(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name, quantity FROM utensils')
    rows = c.fetchall()
    conn.close()
    return [{'name': row[0], 'quantity': row[1]} for row in rows]

def insert_recipe(name, ingredients, utensils, servings, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO recipes (name, ingredients, utensils, servings) VALUES (?, ?, ?, ?)',
              (name, json.dumps(ingredients), json.dumps(utensils), servings))
    conn.commit()
    conn.close()

def fetch_recipes(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name, ingredients, utensils, servings FROM recipes')
    rows = c.fetchall()
    conn.close()
    return [
        {
            'name': row[0],
            'ingredients': json.loads(row[1]),
            'utensils': json.loads(row[2]),
            'servings': row[3]
        } for row in rows
    ]

def migrate_json_to_db():
    # Migrate fridges
    with open(os.path.join(DATA_DIR, 'fridges.json'), 'r', encoding='utf-8') as f:
        fridges = json.load(f)
    for fridge in fridges:
        insert_fridge(fridge['owner'], fridge['fridge_id'], fridge['items'])
    print('Fridges migrated.')

    # Migrate utensils
    with open(os.path.join(DATA_DIR, 'kitchenware.json'), 'r', encoding='utf-8') as f:
        utensils = json.load(f)
    for utensil in utensils:
        insert_utensil(utensil['name'], utensil['quantity'])
    print('Utensils migrated.')

    # Migrate recipes (if structured_recipes.json exists)
    try:
        with open(os.path.join(DATA_DIR, 'structured_recipes.json'), 'r', encoding='utf-8') as f:
            recipes = json.load(f)
        for recipe in recipes:
            insert_recipe(recipe['title'], recipe['steps'], recipe.get('utensils', []), recipe.get('servings', 1))
        print('Recipes migrated.')
    except FileNotFoundError:
        print('structured_recipes.json not found. Skipping recipe migration.')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        init_db()
        migrate_json_to_db()
    else:
        init_db()
        print('Database initialized.') 