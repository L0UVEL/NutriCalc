from django.db import models


class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ('meat', '🥩 Meat & Poultry'),
        ('seafood', '🐟 Seafood'),
        ('dairy', '🥛 Dairy & Eggs'),
        ('grain', '🌾 Grains & Cereals'),
        ('vegetable', '🥦 Vegetables'),
        ('fruit', '🍎 Fruits'),
        ('legume', '🫘 Legumes & Beans'),
        ('nut', '🥜 Nuts & Seeds'),
        ('oil', '🫙 Oils & Fats'),
        ('sweetener', '🍯 Sweeteners'),
        ('beverage', '☕ Beverages'),
        ('condiment', '🧂 Condiments & Spices'),
        ('other', '🍽️ Other'),
    ]

    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    calories_per_100g = models.FloatField(help_text='kcal per 100g')
    protein_g = models.FloatField(default=0.0, help_text='Protein in grams per 100g')
    carbs_g = models.FloatField(default=0.0, help_text='Carbohydrates in grams per 100g')
    fat_g = models.FloatField(default=0.0, help_text='Fat in grams per 100g')
    fiber_g = models.FloatField(default=0.0, help_text='Fiber in grams per 100g')
    sugar_g = models.FloatField(default=0.0, help_text='Sugar in grams per 100g')
    sodium_mg = models.FloatField(default=0.0, help_text='Sodium in mg per 100g')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} kcal/100g)"
