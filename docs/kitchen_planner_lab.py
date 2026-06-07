"""
Smart Kitchen Meal Planner Lab
=============================

Этот файл содержит практические примеры и упражнения для изучения работы
с системой управления холодильником и рекомендаций рецептов.

Инструкция по использованию:
1. Запустите каждую ячейку по порядку
2. Изучите комментарии и код
3. Выполните упражнения
4. Попробуйте изменить параметры и посмотреть результаты
"""

# Импортируем необходимые библиотеки
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from datetime import datetime
from collections import defaultdict
import math

# 1. Основные классы

@dataclass
class Ingredient:
    """Класс для представления ингредиента
    
    Атрибуты:
        name: Название продукта
        quantity: Количество
        unit: Единица измерения
        perishable: Признак скоропортящегося продукта
        expiry_date: Срок годности
        category: Категория продукта
    """
    name: str
    quantity: float
    unit: str
    perishable: bool
    expiry_date: Optional[str]
    category: str

    def __post_init__(self):
        """Проверка корректности данных при создании ингредиента"""
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if self.unit not in ['шт', 'г', 'кг', 'мл', 'л']:
            raise ValueError("Недопустимая единица измерения")

@dataclass
class Fridge:
    """Класс для управления холодильником
    
    Атрибуты:
        fridge_id: Идентификатор холодильника
        owner: Владелец
        items: Список ингредиентов
        capacity: Максимальная вместимость
        temperature: Температура
    """
    fridge_id: str
    owner: str
    items: List[Ingredient]
    capacity: int
    temperature: float

    def add_item(self, item: Ingredient) -> None:
        """Добавление ингредиента в холодильник
        
        Параметры:
            item: Ингредиент для добавления
        
        Исключения:
            ValueError: Если недостаточно места
        """
        # Проверка наличия продукта
        existing = next((i for i in self.items if i.name == item.name), None)
        if existing:
            # Объединение одинаковых продуктов
            if existing.unit == item.unit:
                existing.quantity += item.quantity
            else:
                # Конвертация единиц измерения
                converted = self.convert_units(item.quantity, item.unit, existing.unit)
                existing.quantity += converted
        else:
            # Проверка вместимости
            if self.calculate_total_weight() + item.quantity > self.capacity:
                raise ValueError(f"Недостаточно места в холодильнике. Текущая загрузка: {self.calculate_total_weight()} г")
            # Добавление нового продукта
            self.items.append(item)

    def check_expiry(self) -> List[str]:
        """Проверка сроков годности продуктов
        
        Возвращает:
            Список продуктов с истекшим сроком годности
        """
        today = datetime.now().date()
        expired = []
        for item in self.items:
            if item.expiry_date:
                expiry = datetime.strptime(item.expiry_date, '%Y-%m-%d').date()
                if expiry < today:
                    expired.append(item.name)
        return expired

    def optimize_storage(self) -> None:
        """Оптимизация хранения продуктов
        
        Оптимизация:
            1. Сортировка по категориям
            2. Группировка одинаковых продуктов
            3. Конвертация единиц измерения
        """
        # Сортировка по категориям
        sorted_items = sorted(self.items, key=lambda x: x.category)
        # Группировка
        grouped = defaultdict(list)
        for item in sorted_items:
            grouped[item.category].append(item)
        # Обновление списка
        self.items = [item for group in grouped.values() for item in group]

    def calculate_total_weight(self) -> float:
        """Расчет общей массы продуктов
        
        Возвращает:
            Общая масса продуктов в граммах
        """
        total = 0
        for item in self.items:
            # Конвертируем все в граммы
            if item.unit == 'кг':
                total += item.quantity * 1000
            elif item.unit == 'л':
                total += item.quantity * 1000  # 1 литр = 1000 г
            else:
                total += item.quantity
        return total

    @staticmethod
    def convert_units(value: float, from_unit: str, to_unit: str) -> float:
        """Конвертация единиц измерения
        
        Поддерживаемые конвертации:
            г -> кг
            кг -> г
            мл -> л
            л -> мл
        """
        if from_unit == to_unit:
            return value
        
        conversions = {
            ('г', 'кг'): lambda x: x / 1000,
            ('кг', 'г'): lambda x: x * 1000,
            ('мл', 'л'): lambda x: x / 1000,
            ('л', 'мл'): lambda x: x * 1000
        }
        
        if (from_unit, to_unit) in conversions:
            return conversions[(from_unit, to_unit)](value)
        
        raise ValueError(f"Неподдерживаемая конвертация: {from_unit} -> {to_unit}")

# 2. Пример использования

if __name__ == "__main__":
    print("== Пример использования системы управления холодильником ==")
    
    # Создаем холодильник
    try:
        my_fridge = Fridge(
            fridge_id='fridge_1',
            owner='student',
            items=[],
            capacity=10000,  # максимальная вместимость в граммах
            temperature=4.0  # температура в градусах Цельсия
        )
        
        # Добавляем продукты
        print("\nДобавляем продукты:")
        ingredients = [
            Ingredient('яйца', 6, 'шт', True, '2025-06-15', 'яйца'),
            Ingredient('молоко', 500, 'мл', True, '2025-06-10', 'молоко'),
            Ingredient('мука', 500, 'г', False, None, 'мука'),
            Ingredient('сахар', 200, 'г', False, None, 'сахар'),
            Ingredient('сливочное масло', 100, 'г', True, '2025-06-20', 'масло')
        ]
        
        for ingredient in ingredients:
            try:
                my_fridge.add_item(ingredient)
                print(f"Добавлено: {ingredient.name}")
            except ValueError as e:
                print(f"Ошибка при добавлении {ingredient.name}: {str(e)}")
        
        # Проверяем сроки годности
        print("\nПроверяем сроки годности:")
        expired = my_fridge.check_expiry()
        if expired:
            print(f"Истекшие сроки годности: {expired}")
        else:
            print("Все продукты свежие")
        
        # Оптимизируем хранение
        print("\nОптимизируем хранение:")
        my_fridge.optimize_storage()
        print("\nТекущий инвентарь:")
        for item in my_fridge.items:
            print(f"{item.name}: {item.quantity} {item.unit}")
        
        # Проверяем общую массу
        print(f"\nОбщая масса продуктов: {my_fridge.calculate_total_weight()} г")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

# 3. Упражнения для студентов

def exercise_1():
    """Упражнение 1: Добавление продуктов
    
    Задание:
    1. Создайте новый холодильник
    2. Добавьте следующие продукты:
        - 1 кг муки
        - 200 г сахара
        - 100 г сливочного масла
    3. Проверьте общую массу
    """
    try:
        exercise_fridge = Fridge(
            fridge_id='exercise_1',
            owner='student',
            items=[],
            capacity=10000,
            temperature=4.0
        )
        
        # Добавьте продукты здесь
        # TODO: Добавьте код для добавления продуктов
        
        print("\nРезультат упражнения 1:")
        print(f"Общая масса продуктов: {exercise_fridge.calculate_total_weight()} г")
        
    except Exception as e:
        print(f"Ошибка в упражнении 1: {str(e)}")

def exercise_2():
    """Упражнение 2: Конвертация единиц
    
    Задание:
    1. Создайте функцию для конвертации литров в килограммы
    2. Проверьте работу с водой (1 л = 1 кг)
    3. Проверьте работу с молоком (1 л = 1.03 кг)
    """
    try:
        def convert_l_to_kg(liters: float, density: float = 1.0) -> float:
            """Конвертация литров в килограммы
            
            Параметры:
                liters: Количество литров
                density: Плотность жидкости (по умолчанию 1.0 для воды)
            """
            return liters * density
        
        print("\nРезультат упражнения 2:")
        print(f"1 литр воды = {convert_l_to_kg(1)} кг")
        print(f"1 литр молока = {convert_l_to_kg(1, 1.03)} кг")
        
    except Exception as e:
        print(f"Ошибка в упражнении 2: {str(e)}")

if __name__ == "__main__":
    # Запуск примера
    print("=== Пример работы ===")
    
    # Запуск упражнений
    print("\n=== Упражнения ===")
    exercise_1()
    exercise_2()
