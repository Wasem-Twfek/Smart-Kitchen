from typing import List, Dict, Any

# Hardcoded recipes for initial logic
RECIPES = [
    {
        "name": "Pasta Salad",
        "ingredients": [
            {"name": "pasta", "quantity": 200, "unit": "grams"},
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "lettuce", "quantity": 1, "unit": "head"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Cheese Omelette",
        "ingredients": [
            {"name": "eggs", "quantity": 2, "unit": "pcs"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "milk", "quantity": 50, "unit": "ml"}
        ],
        "utensils": ["frying pan", "spatula", "bowl", "whisk"],
        "servings": 1
    },
    {
        "name": "Chicken Stir Fry",
        "ingredients": [
            {"name": "chicken breast", "quantity": 1, "unit": "pcs"},
            {"name": "rice", "quantity": 100, "unit": "grams"},
            {"name": "lettuce", "quantity": 0.5, "unit": "head"}
        ],
        "utensils": ["frying pan", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Simple Rice",
        "ingredients": [
            {"name": "rice", "quantity": 100, "unit": "grams"}
        ],
        "utensils": ["pot", "bowl"],
        "servings": 1
    },
    # New recipes below
    {
        "name": "Pancake Breakfast",
        "ingredients": [
            {"name": "flour", "quantity": 200, "unit": "grams"},
            {"name": "milk", "quantity": 300, "unit": "ml"},
            {"name": "eggs", "quantity": 2, "unit": "pcs"},
            {"name": "sugar", "quantity": 30, "unit": "grams"},
            {"name": "butter", "quantity": 20, "unit": "grams"}
        ],
        "utensils": ["bowl", "whisk", "frying pan", "spatula"],
        "servings": 4
    },
    {
        "name": "Party Nachos",
        "ingredients": [
            {"name": "tortilla chips", "quantity": 250, "unit": "grams"},
            {"name": "cheese", "quantity": 150, "unit": "grams"},
            {"name": "jalapeno", "quantity": 1, "unit": "pcs"},
            {"name": "salsa", "quantity": 100, "unit": "grams"}
        ],
        "utensils": ["baking tray", "oven", "knife"],
        "servings": 6
    },
    {
        "name": "Vegetable Soup",
        "ingredients": [
            {"name": "carrot", "quantity": 2, "unit": "pcs"},
            {"name": "potato", "quantity": 2, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "celery", "quantity": 2, "unit": "stalks"},
            {"name": "water", "quantity": 1, "unit": "liter"}
        ],
        "utensils": ["pot", "knife", "cutting board", "ladle"],
        "servings": 4
    },
    {
        "name": "Club Sandwich",
        "ingredients": [
            {"name": "bread", "quantity": 6, "unit": "slices"},
            {"name": "chicken breast", "quantity": 1, "unit": "pcs"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"},
            {"name": "tomato", "quantity": 1, "unit": "pcs"},
            {"name": "mayonnaise", "quantity": 30, "unit": "grams"}
        ],
        "utensils": ["knife", "cutting board", "frying pan"],
        "servings": 2
    },
    {
        "name": "Spaghetti Bolognese",
        "ingredients": [
            {"name": "spaghetti", "quantity": 300, "unit": "grams"},
            {"name": "ground beef", "quantity": 250, "unit": "grams"},
            {"name": "tomato sauce", "quantity": 200, "unit": "ml"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "garlic", "quantity": 2, "unit": "cloves"}
        ],
        "utensils": ["pot", "frying pan", "spatula", "knife"],
        "servings": 4
    },
    {
        "name": "Fruit Salad",
        "ingredients": [
            {"name": "apple", "quantity": 2, "unit": "pcs"},
            {"name": "banana", "quantity": 2, "unit": "pcs"},
            {"name": "orange", "quantity": 2, "unit": "pcs"},
            {"name": "grapes", "quantity": 100, "unit": "grams"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 4
    },
    # Additional recipes below
    {
        "name": "Vegetarian Chili",
        "ingredients": [
            {"name": "kidney beans", "quantity": 400, "unit": "grams"},
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "chili powder", "quantity": 1, "unit": "tsp"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 4
    },
    {
        "name": "Greek Salad",
        "ingredients": [
            {"name": "cucumber", "quantity": 1, "unit": "pcs"},
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "feta cheese", "quantity": 100, "unit": "grams"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp"},
            {"name": "olives", "quantity": 50, "unit": "grams"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Beef Tacos",
        "ingredients": [
            {"name": "ground beef", "quantity": 200, "unit": "grams"},
            {"name": "taco shells", "quantity": 6, "unit": "pcs"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "salsa", "quantity": 50, "unit": "grams"}
        ],
        "utensils": ["frying pan", "spatula", "bowl"],
        "servings": 3
    },
    {
        "name": "Vegan Buddha Bowl",
        "ingredients": [
            {"name": "quinoa", "quantity": 100, "unit": "grams"},
            {"name": "chickpeas", "quantity": 100, "unit": "grams"},
            {"name": "spinach", "quantity": 50, "unit": "grams"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "avocado", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["bowl", "pot", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Fish and Chips",
        "ingredients": [
            {"name": "white fish fillet", "quantity": 2, "unit": "pcs"},
            {"name": "potato", "quantity": 3, "unit": "pcs"},
            {"name": "flour", "quantity": 50, "unit": "grams"},
            {"name": "oil", "quantity": 500, "unit": "ml"}
        ],
        "utensils": ["frying pan", "knife", "cutting board", "bowl"],
        "servings": 2
    },
    {
        "name": "Egg Fried Rice",
        "ingredients": [
            {"name": "rice", "quantity": 200, "unit": "grams"},
            {"name": "eggs", "quantity": 2, "unit": "pcs"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "peas", "quantity": 50, "unit": "grams"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp"}
        ],
        "utensils": ["frying pan", "spatula", "bowl"],
        "servings": 2
    },
    {
        "name": "Shakshuka",
        "ingredients": [
            {"name": "eggs", "quantity": 3, "unit": "pcs"},
            {"name": "tomato", "quantity": 3, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp"}
        ],
        "utensils": ["frying pan", "spatula", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Lentil Soup",
        "ingredients": [
            {"name": "lentils", "quantity": 200, "unit": "grams"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "celery", "quantity": 1, "unit": "stalks"},
            {"name": "water", "quantity": 1, "unit": "liter"}
        ],
        "utensils": ["pot", "knife", "cutting board", "ladle"],
        "servings": 4
    },
    {
        "name": "Caprese Salad",
        "ingredients": [
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "mozzarella", "quantity": 100, "unit": "grams"},
            {"name": "basil", "quantity": 10, "unit": "grams"},
            {"name": "olive oil", "quantity": 1, "unit": "tbsp"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Tofu Stir Fry",
        "ingredients": [
            {"name": "tofu", "quantity": 200, "unit": "grams"},
            {"name": "broccoli", "quantity": 100, "unit": "grams"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp"}
        ],
        "utensils": ["frying pan", "spatula", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Classic BLT",
        "ingredients": [
            {"name": "bread", "quantity": 4, "unit": "slices"},
            {"name": "bacon", "quantity": 4, "unit": "slices"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"},
            {"name": "tomato", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["frying pan", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Vegetable Curry",
        "ingredients": [
            {"name": "potato", "quantity": 2, "unit": "pcs"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "peas", "quantity": 50, "unit": "grams"},
            {"name": "curry powder", "quantity": 1, "unit": "tbsp"},
            {"name": "coconut milk", "quantity": 200, "unit": "ml"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Eggplant Parmesan",
        "ingredients": [
            {"name": "eggplant", "quantity": 1, "unit": "pcs"},
            {"name": "tomato sauce", "quantity": 200, "unit": "ml"},
            {"name": "mozzarella", "quantity": 100, "unit": "grams"},
            {"name": "parmesan", "quantity": 30, "unit": "grams"}
        ],
        "utensils": ["baking tray", "oven", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Falafel Wrap",
        "ingredients": [
            {"name": "falafel", "quantity": 6, "unit": "pcs"},
            {"name": "tortilla", "quantity": 2, "unit": "pcs"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"},
            {"name": "tomato", "quantity": 1, "unit": "pcs"},
            {"name": "yogurt", "quantity": 50, "unit": "grams"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Mushroom Risotto",
        "ingredients": [
            {"name": "rice", "quantity": 200, "unit": "grams"},
            {"name": "mushroom", "quantity": 100, "unit": "grams"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "parmesan", "quantity": 30, "unit": "grams"},
            {"name": "butter", "quantity": 20, "unit": "grams"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Chicken Caesar Salad",
        "ingredients": [
            {"name": "chicken breast", "quantity": 1, "unit": "pcs"},
            {"name": "lettuce", "quantity": 1, "unit": "head"},
            {"name": "parmesan", "quantity": 30, "unit": "grams"},
            {"name": "croutons", "quantity": 50, "unit": "grams"},
            {"name": "caesar dressing", "quantity": 30, "unit": "grams"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Tomato Soup",
        "ingredients": [
            {"name": "tomato", "quantity": 4, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "garlic", "quantity": 2, "unit": "cloves"},
            {"name": "water", "quantity": 500, "unit": "ml"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Tuna Sandwich",
        "ingredients": [
            {"name": "bread", "quantity": 4, "unit": "slices"},
            {"name": "tuna", "quantity": 100, "unit": "grams"},
            {"name": "mayonnaise", "quantity": 30, "unit": "grams"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Vegetable Stir Fry",
        "ingredients": [
            {"name": "broccoli", "quantity": 100, "unit": "grams"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp"}
        ],
        "utensils": ["frying pan", "spatula", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Quiche Lorraine",
        "ingredients": [
            {"name": "pie crust", "quantity": 1, "unit": "pcs"},
            {"name": "eggs", "quantity": 3, "unit": "pcs"},
            {"name": "bacon", "quantity": 50, "unit": "grams"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "milk", "quantity": 100, "unit": "ml"}
        ],
        "utensils": ["baking tray", "oven", "bowl", "whisk"],
        "servings": 4
    },
    {
        "name": "Minestrone Soup",
        "ingredients": [
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "celery", "quantity": 1, "unit": "stalks"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "pasta", "quantity": 50, "unit": "grams"},
            {"name": "beans", "quantity": 100, "unit": "grams"},
            {"name": "water", "quantity": 1, "unit": "liter"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 4
    },
    {
        "name": "Avocado Toast",
        "ingredients": [
            {"name": "bread", "quantity": 2, "unit": "slices"},
            {"name": "avocado", "quantity": 1, "unit": "pcs"},
            {"name": "lemon juice", "quantity": 1, "unit": "tbsp"}
        ],
        "utensils": ["knife", "cutting board", "bowl"],
        "servings": 1
    },
    {
        "name": "Peanut Butter Banana Sandwich",
        "ingredients": [
            {"name": "bread", "quantity": 2, "unit": "slices"},
            {"name": "peanut butter", "quantity": 30, "unit": "grams"},
            {"name": "banana", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["knife", "cutting board", "bowl"],
        "servings": 1
    },
    {
        "name": "Vegetable Quesadilla",
        "ingredients": [
            {"name": "tortilla", "quantity": 2, "unit": "pcs"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["frying pan", "spatula", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Chickpea Stew",
        "ingredients": [
            {"name": "chickpeas", "quantity": 200, "unit": "grams"},
            {"name": "tomato", "quantity": 2, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "spices", "quantity": 1, "unit": "tbsp"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Egg Drop Soup",
        "ingredients": [
            {"name": "eggs", "quantity": 2, "unit": "pcs"},
            {"name": "chicken broth", "quantity": 500, "unit": "ml"},
            {"name": "cornstarch", "quantity": 1, "unit": "tbsp"},
            {"name": "spring onion", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["pot", "spoon", "bowl", "whisk"],
        "servings": 2
    },
    {
        "name": "Sweet Potato Fries",
        "ingredients": [
            {"name": "sweet potato", "quantity": 2, "unit": "pcs"},
            {"name": "oil", "quantity": 200, "unit": "ml"},
            {"name": "salt", "quantity": 1, "unit": "tsp"}
        ],
        "utensils": ["baking tray", "oven", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Spinach Frittata",
        "ingredients": [
            {"name": "eggs", "quantity": 4, "unit": "pcs"},
            {"name": "spinach", "quantity": 100, "unit": "grams"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "milk", "quantity": 50, "unit": "ml"}
        ],
        "utensils": ["frying pan", "spatula", "bowl", "whisk"],
        "servings": 3
    },
    {
        "name": "Couscous Salad",
        "ingredients": [
            {"name": "couscous", "quantity": 100, "unit": "grams"},
            {"name": "cucumber", "quantity": 1, "unit": "pcs"},
            {"name": "tomato", "quantity": 1, "unit": "pcs"},
            {"name": "olive oil", "quantity": 1, "unit": "tbsp"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Turkey Wrap",
        "ingredients": [
            {"name": "tortilla", "quantity": 2, "unit": "pcs"},
            {"name": "turkey", "quantity": 100, "unit": "grams"},
            {"name": "lettuce", "quantity": 2, "unit": "leaves"},
            {"name": "cheese", "quantity": 30, "unit": "grams"}
        ],
        "utensils": ["bowl", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Pumpkin Soup",
        "ingredients": [
            {"name": "pumpkin", "quantity": 300, "unit": "grams"},
            {"name": "onion", "quantity": 1, "unit": "pcs"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "water", "quantity": 500, "unit": "ml"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Salmon Teriyaki",
        "ingredients": [
            {"name": "salmon fillet", "quantity": 2, "unit": "pcs"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp"},
            {"name": "rice", "quantity": 100, "unit": "grams"},
            {"name": "broccoli", "quantity": 100, "unit": "grams"}
        ],
        "utensils": ["frying pan", "spatula", "bowl"],
        "servings": 2
    },
    {
        "name": "Potato Gratin",
        "ingredients": [
            {"name": "potato", "quantity": 3, "unit": "pcs"},
            {"name": "cheese", "quantity": 50, "unit": "grams"},
            {"name": "milk", "quantity": 100, "unit": "ml"},
            {"name": "butter", "quantity": 20, "unit": "grams"}
        ],
        "utensils": ["baking tray", "oven", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Stuffed Peppers",
        "ingredients": [
            {"name": "bell pepper", "quantity": 2, "unit": "pcs"},
            {"name": "rice", "quantity": 100, "unit": "grams"},
            {"name": "ground beef", "quantity": 100, "unit": "grams"},
            {"name": "tomato sauce", "quantity": 100, "unit": "ml"}
        ],
        "utensils": ["baking tray", "oven", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Pasta Primavera",
        "ingredients": [
            {"name": "pasta", "quantity": 200, "unit": "grams"},
            {"name": "zucchini", "quantity": 1, "unit": "pcs"},
            {"name": "carrot", "quantity": 1, "unit": "pcs"},
            {"name": "peas", "quantity": 50, "unit": "grams"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "French Toast",
        "ingredients": [
            {"name": "bread", "quantity": 4, "unit": "slices"},
            {"name": "eggs", "quantity": 2, "unit": "pcs"},
            {"name": "milk", "quantity": 50, "unit": "ml"},
            {"name": "sugar", "quantity": 20, "unit": "grams"}
        ],
        "utensils": ["frying pan", "spatula", "bowl", "whisk"],
        "servings": 2
    },
    {
        "name": "Vegetable Paella",
        "ingredients": [
            {"name": "rice", "quantity": 200, "unit": "grams"},
            {"name": "peas", "quantity": 50, "unit": "grams"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "tomato", "quantity": 1, "unit": "pcs"},
            {"name": "saffron", "quantity": 1, "unit": "tsp"}
        ],
        "utensils": ["pot", "spoon", "knife", "cutting board"],
        "servings": 3
    },
    {
        "name": "Chicken Fajitas",
        "ingredients": [
            {"name": "chicken breast", "quantity": 1, "unit": "pcs"},
            {"name": "tortilla", "quantity": 2, "unit": "pcs"},
            {"name": "bell pepper", "quantity": 1, "unit": "pcs"},
            {"name": "onion", "quantity": 1, "unit": "pcs"}
        ],
        "utensils": ["frying pan", "spatula", "knife", "cutting board"],
        "servings": 2
    },
    {
        "name": "Miso Soup",
        "ingredients": [
            {"name": "miso paste", "quantity": 30, "unit": "grams"},
            {"name": "tofu", "quantity": 50, "unit": "grams"},
            {"name": "spring onion", "quantity": 1, "unit": "pcs"},
            {"name": "water", "quantity": 500, "unit": "ml"}
        ],
        "utensils": ["pot", "spoon", "bowl"],
        "servings": 2
    }
]

class RecipePlanner:
    def __init__(self, recipes: List[Dict[str, Any]]):
        self.recipes = recipes

    def recommend(self, inventory: List[Dict[str, Any]], utensils: List[str], servings: int) -> Dict[str, Any]:
        """
        Recommend the best recipe based on available inventory, utensils, and servings.
        Returns a dict with recipe, missing_ingredients, and missing_utensils.
        """
        best_match = None
        best_score = -1
        best_missing = None
        for recipe in self.recipes:
            if servings > recipe["servings"]:
                continue  # skip recipes with too few servings
            missing_ingredients = []
            for req in recipe["ingredients"]:
                found = False
                for item in inventory:
                    if item["name"] == req["name"] and item["unit"] == req["unit"] and item["quantity"] >= req["quantity"]:
                        found = True
                        break
                if not found:
                    missing_ingredients.append(req)
            missing_utensils = [u for u in recipe["utensils"] if u not in utensils]
            score = len(recipe["ingredients"]) - len(missing_ingredients)  # simple score: more available ingredients is better
            if score > best_score:
                best_score = score
                best_match = recipe
                best_missing = {
                    "ingredients": missing_ingredients,
                    "utensils": missing_utensils
                }
        return {
            "recipe": best_match,
            "missing_ingredients": best_missing["ingredients"] if best_missing else [],
            "missing_utensils": best_missing["utensils"] if best_missing else []
        } 