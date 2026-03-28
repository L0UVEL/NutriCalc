from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'servings', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    inlines = [RecipeIngredientInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient_name', 'quantity_g', 'recipe']
    list_filter = ['recipe']
    search_fields = ['ingredient_name']
