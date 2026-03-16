from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    instructions = models.TextField(blank=True, default='')
    servings = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient_name = models.CharField(max_length=200)
    quantity_g = models.FloatField(help_text='Quantity in grams')

    class Meta:
        ordering = ['ingredient_name']

    def __str__(self):
        return f"{self.ingredient_name} ({self.quantity_g}g) in {self.recipe.name}"
