from django.contrib import admin
from .models import Recipe, RecipeIngredient

print("DEBUG: Loading recipes/admin.py...")

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'servings', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    inlines = [RecipeIngredientInline]

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient_name', 'quantity_g', 'recipe']
    list_filter = ['recipe']
    search_fields = ['ingredient_name']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)

print("DEBUG: Recipes models registered in Admin.")
