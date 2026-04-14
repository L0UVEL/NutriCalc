import django, os, sys
import sqlite3

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutri_calc.settings')
django.setup()

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print("Migrating Ingredients...")
Ingredient.objects.using('mongodb').all().delete()
c.execute("SELECT * FROM ingredients_ingredient")
for row in c.fetchall():
    Ingredient.objects.using('mongodb').create(
        name=row['name'],
        category=row['category'],
        calories_per_100g=row['calories_per_100g'],
        protein_g=row['protein_g'],
        carbs_g=row['carbs_g'],
        fat_g=row['fat_g'],
        fiber_g=row['fiber_g'],
        sugar_g=row['sugar_g'],
        sodium_mg=row['sodium_mg'],
        description=row['description'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )

print("Migrating Recipes...")
Recipe.objects.using('mongodb').all().delete()
RecipeIngredient.objects.using('mongodb').all().delete()

# Map old recipe id (int) to new Recipe object
recipe_map = {}

c.execute("SELECT * FROM recipes_recipe")
for row in c.fetchall():
    new_rec = Recipe.objects.using('mongodb').create(
        name=row['name'],
        description=row['description'],
        instructions=row['instructions'],
        servings=row['servings'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )
    recipe_map[row['id']] = new_rec

print("Migrating Recipe Ingredients...")
c.execute("SELECT * FROM recipes_recipeingredient")
for row in c.fetchall():
    if row['recipe_id'] in recipe_map:
        RecipeIngredient.objects.using('mongodb').create(
            recipe=recipe_map[row['recipe_id']],
            ingredient_name=row['ingredient_name'],
            quantity_g=row['quantity_g']
        )

print(f"Data transferred! Ingredients in Mongo: {Ingredient.objects.using('mongodb').count()}")
