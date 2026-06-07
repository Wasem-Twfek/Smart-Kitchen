# Техническое описание Smart Kitchen Meal Planner

## 1. Архитектура системы

### 1.1. Основные компоненты

Система состоит из следующих основных компонентов:

1. **Бэкенд**
   - `fridge.py`: Управление инвентарем холодильников
   - `planner.py`: Система рекомендаций рецептов
   - `order.py`: Управление списком покупок
   - `db.py`: Работа с базой данных SQLite
   - `nlp/`: Модули обработки естественного языка для анализа рецептов

2. **База данных**
   - Таблицы: `fridges`, `utensils`, `recipes`, `users`
   - JSON-структуры для хранения ингредиентов и утвари
   - Индексы для быстрого поиска

3. **Веб-интерфейс**
   - Flask + SocketIO для реального времени
   - Модульная структура шаблонов HTML
   - REST API для взаимодействия с мобильным приложением

## 2. Описание алгоритмов

### 2.1. Управление инвентарем (fridge.py)

```python
# Структура данных для ингредиентов
@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: str
    perishable: bool
    expiry_date: Optional[str]
    category: str  # категория продукта (овощи, мясо, молоко и т.д.)
    
# Методы работы с ингредиентами
def add_item(self, item: Ingredient) -> None:
    """Добавление ингредиента в инвентарь"""
    # Проверка наличия продукта
    existing = self.find_item(item.name)
    if existing:
        # Объединение одинаковых продуктов
        if existing.unit == item.unit:
            existing.quantity += item.quantity
        else:
            # Конвертация единиц измерения
            converted = self.convert_units(item.quantity, item.unit, existing.unit)
            existing.quantity += converted
    else:
        # Добавление нового продукта
        self.items.append(item)

def check_availability(self, ingredients: List[Ingredient]) -> Tuple[bool, List[str]]:
    """Проверка наличия ингредиентов"""
    missing = []
    for ingredient in ingredients:
        existing = self.find_item(ingredient.name)
        if not existing or existing.quantity < ingredient.quantity:
            missing.append(ingredient.name)
    return len(missing) == 0, missing
```

### 2.2. Система рекомендаций (planner.py)

```python
def recommend_recipes(self, available_ingredients: List[Ingredient], 
                     available_utensils: List[str], servings: int) -> List[Dict]:
    """Основной алгоритм рекомендаций рецептов"""
    recommendations = []
    
    # 1. Фильтрация по доступным ингредиентам
    filtered_recipes = self.filter_by_ingredients(available_ingredients)
    
    # 2. Проверка наличия утвари
    utensil_filtered = self.filter_by_utensils(filtered_recipes, available_utensils)
    
    # 3. Масштабирование порций
    scaled_recipes = [self.scale_recipe(recipe, servings) 
                     for recipe in utensil_filtered]
    
    # 4. Оценка совместимости ингредиентов
    for recipe in scaled_recipes:
        score = self.calculate_compatibility(recipe, available_ingredients)
        if score > 0.7:  # Минимальный порог совместимости
            recommendations.append({
                'recipe': recipe,
                'score': score,
                'missing_ingredients': self.find_missing_ingredients(recipe, available_ingredients),
                'missing_utensils': self.find_missing_utensils(recipe, available_utensils)
            })
    
    # 5. Сортировка по релевантности
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:5]  # Возвращаем топ-5 рецептов

# Вспомогательные методы
def calculate_compatibility(self, recipe: Dict, available: List[Ingredient]) -> float:
    """Расчет совместимости рецепта с доступными ингредиентами"""
    total_score = 0
    
    # Оценка совпадения ингредиентов
    ingredient_score = len(set(recipe['ingredients']) & set(available)) / len(recipe['ingredients'])
    
    # Оценка совпадения категорий продуктов
    category_score = self.calculate_category_score(recipe, available)
    
    # Оценка сроков годности
    expiry_score = self.calculate_expiry_score(recipe, available)
    
    total_score = 0.5 * ingredient_score + 0.3 * category_score + 0.2 * expiry_score
    return total_score

# Методы для работы с утварью
def find_missing_utensils(self, recipe: Dict, available: List[str]) -> List[str]:
    """Поиск недостающей утвари для рецепта"""
    return [utensil for utensil in recipe['utensils'] if utensil not in available]

# Методы для работы с ингредиентами
def find_missing_ingredients(self, recipe: Dict, available: List[Ingredient]) -> List[str]:
    """Поиск недостающих ингредиентов"""
    missing = []
    for ingredient in recipe['ingredients']:
        if not any(i.name == ingredient['name'] and i.quantity >= ingredient['quantity'] 
                   for i in available):
            missing.append(ingredient['name'])
    return missing
```

## 3. Примеры использования

### 3.1. Пример 1: Управление инвентарем

```python
# Инициализация холодильника
fridge = FridgeManager()

# Добавление ингредиентов
fridge.add_item(
    Ingredient(
        name="яйца",
        quantity=6,
        unit="шт",
        perishable=True,
        expiry_date="2025-02-15",
        category="яйца"
    )
)

# Проверка наличия ингредиентов
available, missing = fridge.check_availability([
    Ingredient(
        name="яйца",
        quantity=2,
        unit="шт",
        perishable=True,
        category="яйца"
    ),
    Ingredient(
        name="молоко",
        quantity=200,
        unit="мл",
        perishable=True,
        category="молоко"
    )
])

# Объединение инвентарей из разных холодильников
fridge.merge_inventories([
    {
        "fridge_id": "fridge_1",
        "items": [
            {"name": "яйца", "quantity": 6, "unit": "шт"},
            {"name": "молоко", "quantity": 500, "unit": "мл"}
        ]
    },
    {
        "fridge_id": "fridge_2",
        "items": [
            {"name": "мука", "quantity": 500, "unit": "г"},
            {"name": "сахар", "quantity": 200, "unit": "г"}
        ]
    }
])
```

### 3.2. Пример 2: Рекомендация рецептов

```python
# Доступные ингредиенты
available_ingredients = [
    Ingredient(
        name="яйца",
        quantity=6,
        unit="шт",
        perishable=True,
        category="яйца"
    ),
    Ingredient(
        name="молоко",
        quantity=500,
        unit="мл",
        perishable=True,
        category="молоко"
    ),
    Ingredient(
        name="мука",
        quantity=500,
        unit="г",
        perishable=False,
        category="мука"
    )
]

# Доступная утварь
available_utensils = ["сковорода", "миска", "вилка", "миксер"]

# Получение рекомендаций
recommendations = planner.recommend_recipes(
    available_ingredients=available_ingredients,
    available_utensils=available_utensils,
    servings=4
)

# Вывод результатов
for rec in recommendations:
    print(f"Рецепт: {rec['recipe']['name']}")
    print(f"Совместимость: {rec['score']:.2f}")
    print("Недостающие ингредиенты:", rec['missing_ingredients'])
    print("Недостающая утварь:", rec['missing_utensils'])
    print("---")

# Пример вывода:
# Рецепт: Омлет
# Совместимость: 0.95
# Недостающие ингредиенты: ['соль']
# Недостающая утварь: ['лопатка']
# ---
# Рецепт: Блинчики
# Совместимость: 0.85
# Недостающие ингредиенты: ['сахар']
# Недостающая утварь: ['лопатка']
```

## 4. Структура данных

### 4.1. Структура рецепта

```python
@dataclass
class Recipe:
    name: str
    description: str
    ingredients: List[Ingredient]
    utensils: List[str]
    servings: int
    preparation_time: int  # в минутах
    cooking_time: int  # в минутах
    difficulty: int  # от 1 до 5
    category: str  # категория блюда (завтрак, обед, ужин)
    tags: List[str]  # теги для поиска
    
    # Методы класса
    def scale(self, new_servings: int) -> None:
        """Масштабирование рецепта для нового количества порций"""
        ratio = new_servings / self.servings
        for ingredient in self.ingredients:
            ingredient.quantity *= ratio
        self.servings = new_servings

    def calculate_total_time(self) -> int:
        """Расчет общего времени приготовления"""
        return self.preparation_time + self.cooking_time

    def get_nutrition_info(self) -> Dict:
        """Получение информации о питательной ценности"""
        return {
            'calories': self.calculate_calories(),
            'protein': self.calculate_protein(),
            'fat': self.calculate_fat(),
            'carbs': self.calculate_carbs()
        }
```

### 4.2. Структура холодильника

```python
@dataclass
class Fridge:
    fridge_id: str
    owner: str
    items: List[Ingredient]
    capacity: int  # максимальная вместимость в граммах
    temperature: float  # текущая температура
    
    # Методы класса
    def add_item(self, item: Ingredient) -> None:
        """Добавление ингредиента с проверкой вместимости"""
        if self.calculate_total_weight() + item.quantity <= self.capacity:
            self.items.append(item)
        else:
            raise ValueError("Недостаточно места в холодильнике")

    def calculate_total_weight(self) -> float:
        """Расчет общей массы продуктов"""
        return sum(item.quantity for item in self.items)

    def check_expiry(self) -> List[str]:
        """Проверка сроков годности"""
        today = datetime.now().date()
        expired = []
        for item in self.items:
            if item.expiry_date and datetime.strptime(item.expiry_date, '%Y-%m-%d').date() < today:
                expired.append(item.name)
        return expired

    def optimize_storage(self) -> None:
        """Оптимизация хранения продуктов"""
        # Сортировка продуктов по категориям
        sorted_items = sorted(self.items, key=lambda x: x.category)
        # Группировка по категориям
        grouped = defaultdict(list)
        for item in sorted_items:
            grouped[item.category].append(item)
        # Обновление списка
        self.items = [item for group in grouped.values() for item in group]
```

### 4.3. Структура базы данных

```sql
-- Таблица холодильников
CREATE TABLE fridges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT NOT NULL,
    fridge_id TEXT UNIQUE NOT NULL,
    capacity INTEGER NOT NULL,
    temperature REAL NOT NULL,
    items TEXT NOT NULL,  -- JSON строка
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица рецептов
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    ingredients TEXT NOT NULL,  -- JSON строка
    utensils TEXT NOT NULL,     -- JSON строка
    servings INTEGER NOT NULL,
    preparation_time INTEGER NOT NULL,
    cooking_time INTEGER NOT NULL,
    difficulty INTEGER NOT NULL,
    category TEXT NOT NULL,
    tags TEXT,                 -- JSON строка
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица утвари
CREATE TABLE utensils (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для быстрого поиска
CREATE INDEX idx_fridges_owner ON fridges(owner);
CREATE INDEX idx_recipes_category ON recipes(category);
CREATE INDEX idx_recipes_tags ON recipes(tags);
CREATE INDEX idx_utensils_name ON utensils(name);
```

## 5. Функции системы

### 5.1. Основные функции

1. **Управление инвентарем**
   - Добавление/удаление ингредиентов
   - Отслеживание сроков годности
   - Автоматическое объединение инвентарей

2. **Рекомендации рецептов**
   - Фильтрация по доступным ингредиентам
   - Проверка наличия утвари
   - Масштабирование порций
   - Оценка совместимости ингредиентов

3. **Список покупок**
   - Автоматическое создание списка
   - Планирование покупок
   - Интеграция с системой заказов

### 5.2. Продвинутые функции

1. **Умное распределение ресурсов**
   - Оптимизация использования ингредиентов
   - Минимизация отходов
   - Автоматическое планирование меню

2. **Интеграция с IoT**
   - Синхронизация с умными холодильниками
   - Автоматическое отслеживание запасов
   - Уведомления о низком уровне продуктов

## 6. Примеры вывода системы

### 6.1. Рекомендации рецептов

```python
# Пример вывода системы
recommendations = [
    {
        "recipe": "Омлет",
        "score": 0.95,
        "missing_ingredients": [],
        "missing_utensils": [],
        "servings": 2
    },
    {
        "recipe": "Блинчики",
        "score": 0.85,
        "missing_ingredients": ["сахар"],
        "missing_utensils": ["лопатка"],
        "servings": 4
    }
]
```

### 6.2. Список покупок

```python
shopping_list = {
    "ingredients": [
        {"name": "сахар", "quantity": 100, "unit": "г"},
        {"name": "соль", "quantity": 50, "unit": "г"}
    ],
    "utensils": ["лопатка", "миксер"]
}
```

## 7. Возможные улучшения

1. **Расширение функционала**
   - Добавление поддержки разных систем измерений
   - Интеграция с системами доставки
   - Добавление функции сканирования штрих-кодов

2. **Оптимизация алгоритмов**
   - Улучшение системы рекомендаций
   - Оптимизация поиска похожих рецептов
   - Добавление машинного обучения для предсказания предпочтений

3. **Расширение базы данных**
   - Добавление большего количества рецептов
   - Интеграция с внешними базами данных рецептов
   - Добавление пользовательских рецептов
