from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


SEED_DATA = [
    # Meat & Poultry
    {"name": "Chicken Breast (cooked)", "category": "meat", "calories_per_100g": 165, "protein_g": 31.0, "carbs_g": 0.0, "fat_g": 3.6, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 74},
    {"name": "Chicken Thigh (cooked)", "category": "meat", "calories_per_100g": 209, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 10.9, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 91},
    {"name": "Ground Beef (80/20)", "category": "meat", "calories_per_100g": 254, "protein_g": 17.2, "carbs_g": 0.0, "fat_g": 20.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 75},
    {"name": "Beef Sirloin", "category": "meat", "calories_per_100g": 207, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 11.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 57},
    {"name": "Pork Loin", "category": "meat", "calories_per_100g": 242, "protein_g": 27.0, "carbs_g": 0.0, "fat_g": 14.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 63},
    {"name": "Bacon (cooked)", "category": "meat", "calories_per_100g": 541, "protein_g": 37.0, "carbs_g": 1.4, "fat_g": 42.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 1717},
    {"name": "Turkey Breast", "category": "meat", "calories_per_100g": 135, "protein_g": 30.0, "carbs_g": 0.0, "fat_g": 1.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 70},
    {"name": "Lamb Shoulder", "category": "meat", "calories_per_100g": 258, "protein_g": 25.0, "carbs_g": 0.0, "fat_g": 17.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 72},
    # Seafood
    {"name": "Salmon (Atlantic)", "category": "seafood", "calories_per_100g": 208, "protein_g": 20.4, "carbs_g": 0.0, "fat_g": 13.4, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 59},
    {"name": "Tuna (canned in water)", "category": "seafood", "calories_per_100g": 116, "protein_g": 26.0, "carbs_g": 0.0, "fat_g": 0.8, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 337},
    {"name": "Shrimp (cooked)", "category": "seafood", "calories_per_100g": 99, "protein_g": 24.0, "carbs_g": 0.3, "fat_g": 0.3, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 111},
    {"name": "Tilapia", "category": "seafood", "calories_per_100g": 96, "protein_g": 20.1, "carbs_g": 0.0, "fat_g": 1.7, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 52},
    {"name": "Cod", "category": "seafood", "calories_per_100g": 82, "protein_g": 18.0, "carbs_g": 0.0, "fat_g": 0.7, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 54},
    {"name": "Sardines (canned)", "category": "seafood", "calories_per_100g": 208, "protein_g": 24.6, "carbs_g": 0.0, "fat_g": 11.5, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 505},
    # Dairy & Eggs
    {"name": "Whole Egg", "category": "dairy", "calories_per_100g": 155, "protein_g": 13.0, "carbs_g": 1.1, "fat_g": 10.6, "fiber_g": 0, "sugar_g": 1.1, "sodium_mg": 124},
    {"name": "Egg White", "category": "dairy", "calories_per_100g": 52, "protein_g": 10.9, "carbs_g": 0.7, "fat_g": 0.2, "fiber_g": 0, "sugar_g": 0.7, "sodium_mg": 166},
    {"name": "Whole Milk", "category": "dairy", "calories_per_100g": 61, "protein_g": 3.2, "carbs_g": 4.8, "fat_g": 3.3, "fiber_g": 0, "sugar_g": 5.0, "sodium_mg": 43},
    {"name": "Greek Yogurt (plain)", "category": "dairy", "calories_per_100g": 59, "protein_g": 10.0, "carbs_g": 3.6, "fat_g": 0.4, "fiber_g": 0, "sugar_g": 3.2, "sodium_mg": 36},
    {"name": "Cheddar Cheese", "category": "dairy", "calories_per_100g": 402, "protein_g": 25.0, "carbs_g": 1.3, "fat_g": 33.0, "fiber_g": 0, "sugar_g": 0.5, "sodium_mg": 621},
    {"name": "Mozzarella Cheese", "category": "dairy", "calories_per_100g": 280, "protein_g": 28.0, "carbs_g": 2.2, "fat_g": 17.0, "fiber_g": 0, "sugar_g": 1.0, "sodium_mg": 486},
    {"name": "Butter (unsalted)", "category": "dairy", "calories_per_100g": 717, "protein_g": 0.9, "carbs_g": 0.1, "fat_g": 81.0, "fiber_g": 0, "sugar_g": 0.1, "sodium_mg": 11},
    {"name": "Cream Cheese", "category": "dairy", "calories_per_100g": 342, "protein_g": 6.2, "carbs_g": 4.1, "fat_g": 34.0, "fiber_g": 0, "sugar_g": 3.2, "sodium_mg": 251},
    # Grains
    {"name": "White Rice (cooked)", "category": "grain", "calories_per_100g": 130, "protein_g": 2.7, "carbs_g": 28.2, "fat_g": 0.3, "fiber_g": 0.4, "sugar_g": 0, "sodium_mg": 1},
    {"name": "Brown Rice (cooked)", "category": "grain", "calories_per_100g": 111, "protein_g": 2.6, "carbs_g": 23.0, "fat_g": 0.9, "fiber_g": 1.8, "sugar_g": 0, "sodium_mg": 5},
    {"name": "Oats (dry)", "category": "grain", "calories_per_100g": 389, "protein_g": 17.0, "carbs_g": 66.0, "fat_g": 7.0, "fiber_g": 10.6, "sugar_g": 0, "sodium_mg": 2},
    {"name": "Whole Wheat Bread", "category": "grain", "calories_per_100g": 247, "protein_g": 13.0, "carbs_g": 41.0, "fat_g": 4.2, "fiber_g": 6.0, "sugar_g": 5.7, "sodium_mg": 400},
    {"name": "Pasta (cooked)", "category": "grain", "calories_per_100g": 158, "protein_g": 5.8, "carbs_g": 30.9, "fat_g": 0.9, "fiber_g": 1.8, "sugar_g": 0.6, "sodium_mg": 1},
    {"name": "Quinoa (cooked)", "category": "grain", "calories_per_100g": 120, "protein_g": 4.4, "carbs_g": 21.3, "fat_g": 1.9, "fiber_g": 2.8, "sugar_g": 0.9, "sodium_mg": 7},
    {"name": "Corn Tortilla", "category": "grain", "calories_per_100g": 218, "protein_g": 5.7, "carbs_g": 45.9, "fat_g": 2.5, "fiber_g": 6.3, "sugar_g": 0.9, "sodium_mg": 309},
    # Vegetables
    {"name": "Broccoli", "category": "vegetable", "calories_per_100g": 34, "protein_g": 2.8, "carbs_g": 6.6, "fat_g": 0.4, "fiber_g": 2.6, "sugar_g": 1.7, "sodium_mg": 33},
    {"name": "Spinach (raw)", "category": "vegetable", "calories_per_100g": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4, "fiber_g": 2.2, "sugar_g": 0.4, "sodium_mg": 79},
    {"name": "Sweet Potato", "category": "vegetable", "calories_per_100g": 86, "protein_g": 1.6, "carbs_g": 20.1, "fat_g": 0.1, "fiber_g": 3.0, "sugar_g": 4.2, "sodium_mg": 55},
    {"name": "Carrot", "category": "vegetable", "calories_per_100g": 41, "protein_g": 0.9, "carbs_g": 9.6, "fat_g": 0.2, "fiber_g": 2.8, "sugar_g": 4.7, "sodium_mg": 69},
    {"name": "White Onion", "category": "vegetable", "calories_per_100g": 40, "protein_g": 1.1, "carbs_g": 9.3, "fat_g": 0.1, "fiber_g": 1.7, "sugar_g": 4.2, "sodium_mg": 4},
    {"name": "Garlic", "category": "vegetable", "calories_per_100g": 149, "protein_g": 6.4, "carbs_g": 33.1, "fat_g": 0.5, "fiber_g": 2.1, "sugar_g": 1.0, "sodium_mg": 17},
    {"name": "Tomato (raw)", "category": "vegetable", "calories_per_100g": 18, "protein_g": 0.9, "carbs_g": 3.9, "fat_g": 0.2, "fiber_g": 1.2, "sugar_g": 2.6, "sodium_mg": 5},
    {"name": "Bell Pepper (red)", "category": "vegetable", "calories_per_100g": 31, "protein_g": 1.0, "carbs_g": 6.0, "fat_g": 0.3, "fiber_g": 2.1, "sugar_g": 4.2, "sodium_mg": 4},
    {"name": "Cucumber", "category": "vegetable", "calories_per_100g": 15, "protein_g": 0.7, "carbs_g": 3.6, "fat_g": 0.1, "fiber_g": 0.5, "sugar_g": 1.7, "sodium_mg": 2},
    {"name": "Mushroom (white)", "category": "vegetable", "calories_per_100g": 22, "protein_g": 3.1, "carbs_g": 3.3, "fat_g": 0.3, "fiber_g": 1.0, "sugar_g": 2.0, "sodium_mg": 5},
    {"name": "Kale (raw)", "category": "vegetable", "calories_per_100g": 49, "protein_g": 4.3, "carbs_g": 8.8, "fat_g": 0.9, "fiber_g": 3.6, "sugar_g": 2.3, "sodium_mg": 38},
    {"name": "Eggplant", "category": "vegetable", "calories_per_100g": 25, "protein_g": 1.0, "carbs_g": 6.0, "fat_g": 0.2, "fiber_g": 3.0, "sugar_g": 3.5, "sodium_mg": 2},
    # Fruits
    {"name": "Banana", "category": "fruit", "calories_per_100g": 89, "protein_g": 1.1, "carbs_g": 23.0, "fat_g": 0.3, "fiber_g": 2.6, "sugar_g": 12.2, "sodium_mg": 1},
    {"name": "Apple (with skin)", "category": "fruit", "calories_per_100g": 52, "protein_g": 0.3, "carbs_g": 13.8, "fat_g": 0.2, "fiber_g": 2.4, "sugar_g": 10.4, "sodium_mg": 1},
    {"name": "Avocado", "category": "fruit", "calories_per_100g": 160, "protein_g": 2.0, "carbs_g": 8.5, "fat_g": 14.7, "fiber_g": 6.7, "sugar_g": 0.7, "sodium_mg": 7},
    {"name": "Strawberry", "category": "fruit", "calories_per_100g": 32, "protein_g": 0.7, "carbs_g": 7.7, "fat_g": 0.3, "fiber_g": 2.0, "sugar_g": 4.9, "sodium_mg": 1},
    {"name": "Blueberry", "category": "fruit", "calories_per_100g": 57, "protein_g": 0.7, "carbs_g": 14.5, "fat_g": 0.3, "fiber_g": 2.4, "sugar_g": 10.0, "sodium_mg": 1},
    {"name": "Mango", "category": "fruit", "calories_per_100g": 60, "protein_g": 0.8, "carbs_g": 15.0, "fat_g": 0.4, "fiber_g": 1.6, "sugar_g": 13.7, "sodium_mg": 1},
    {"name": "Orange", "category": "fruit", "calories_per_100g": 47, "protein_g": 0.9, "carbs_g": 11.8, "fat_g": 0.1, "fiber_g": 2.4, "sugar_g": 9.4, "sodium_mg": 0},
    # Legumes
    {"name": "Chickpeas (cooked)", "category": "legume", "calories_per_100g": 164, "protein_g": 8.9, "carbs_g": 27.4, "fat_g": 2.6, "fiber_g": 7.6, "sugar_g": 4.8, "sodium_mg": 7},
    {"name": "Black Beans (cooked)", "category": "legume", "calories_per_100g": 132, "protein_g": 8.9, "carbs_g": 23.7, "fat_g": 0.5, "fiber_g": 8.7, "sugar_g": 0.3, "sodium_mg": 1},
    {"name": "Lentils (cooked)", "category": "legume", "calories_per_100g": 116, "protein_g": 9.0, "carbs_g": 20.1, "fat_g": 0.4, "fiber_g": 7.9, "sugar_g": 1.8, "sodium_mg": 2},
    {"name": "Tofu (firm)", "category": "legume", "calories_per_100g": 76, "protein_g": 8.1, "carbs_g": 1.9, "fat_g": 4.8, "fiber_g": 0.3, "sugar_g": 0.5, "sodium_mg": 7},
    # Nuts & Seeds
    {"name": "Almonds", "category": "nut", "calories_per_100g": 579, "protein_g": 21.2, "carbs_g": 21.6, "fat_g": 49.9, "fiber_g": 12.5, "sugar_g": 4.4, "sodium_mg": 1},
    {"name": "Walnuts", "category": "nut", "calories_per_100g": 654, "protein_g": 15.2, "carbs_g": 13.7, "fat_g": 65.2, "fiber_g": 6.7, "sugar_g": 2.6, "sodium_mg": 2},
    {"name": "Chia Seeds", "category": "nut", "calories_per_100g": 486, "protein_g": 16.5, "carbs_g": 42.1, "fat_g": 30.7, "fiber_g": 34.4, "sugar_g": 0, "sodium_mg": 16},
    {"name": "Peanut Butter", "category": "nut", "calories_per_100g": 588, "protein_g": 25.0, "carbs_g": 20.0, "fat_g": 50.0, "fiber_g": 6.0, "sugar_g": 9.0, "sodium_mg": 365},
    # Oils
    {"name": "Olive Oil", "category": "oil", "calories_per_100g": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 2},
    {"name": "Coconut Oil", "category": "oil", "calories_per_100g": 862, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0},
    {"name": "Vegetable Oil", "category": "oil", "calories_per_100g": 884, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 100.0, "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0},
    # Sweeteners
    {"name": "White Sugar", "category": "sweetener", "calories_per_100g": 387, "protein_g": 0.0, "carbs_g": 100.0, "fat_g": 0.0, "fiber_g": 0, "sugar_g": 100.0, "sodium_mg": 1},
    {"name": "Honey", "category": "sweetener", "calories_per_100g": 304, "protein_g": 0.3, "carbs_g": 82.4, "fat_g": 0.0, "fiber_g": 0.2, "sugar_g": 82.1, "sodium_mg": 4},
    {"name": "Brown Sugar", "category": "sweetener", "calories_per_100g": 380, "protein_g": 0.1, "carbs_g": 98.1, "fat_g": 0.0, "fiber_g": 0, "sugar_g": 97.0, "sodium_mg": 28},
    # Condiments
    {"name": "Soy Sauce", "category": "condiment", "calories_per_100g": 53, "protein_g": 5.0, "carbs_g": 4.9, "fat_g": 0.1, "fiber_g": 0.4, "sugar_g": 0.9, "sodium_mg": 5637},
    {"name": "Tomato Sauce (canned)", "category": "condiment", "calories_per_100g": 32, "protein_g": 1.6, "carbs_g": 7.1, "fat_g": 0.2, "fiber_g": 1.5, "sugar_g": 4.7, "sodium_mg": 317},
    {"name": "Mayonnaise", "category": "condiment", "calories_per_100g": 680, "protein_g": 1.0, "carbs_g": 0.6, "fat_g": 75.0, "fiber_g": 0, "sugar_g": 0.4, "sodium_mg": 635},
    {"name": "Hot Sauce", "category": "condiment", "calories_per_100g": 21, "protein_g": 0.9, "carbs_g": 4.0, "fat_g": 0.3, "fiber_g": 0.5, "sugar_g": 0.3, "sodium_mg": 2315},
]


class Command(BaseCommand):
    help = 'Seeds the database with 65+ common ingredients'

    def handle(self, *args, **options):
        created = 0
        skipped = 0
        for data in SEED_DATA:
            obj, new = Ingredient.objects.get_or_create(name=data['name'], defaults=data)
            if new:
                created += 1
            else:
                skipped += 1
        self.stdout.write(self.style.SUCCESS(
            f'[OK] Seeding complete: {created} created, {skipped} already existed.'
        ))
