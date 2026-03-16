from django.contrib import admin
from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories_per_100g', 'protein_g', 'carbs_g', 'fat_g']
    list_filter = ['category']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_per_page = 30
