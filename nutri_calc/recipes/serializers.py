from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        # Omit recipe to make it cleaner when nested or accessed separately
        fields = ['id', 'ingredient_name', 'quantity_g']

class RecipeSerializer(serializers.ModelSerializer):
    # This matches the related_name='recipe_ingredients' in the model
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'instructions', 'servings', 'created_at', 'updated_at', 'recipe_ingredients']
