from django import forms
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            'name', 'category', 'calories_per_100g',
            'protein_g', 'carbs_g', 'fat_g', 'fiber_g',
            'sugar_g', 'sodium_mg', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Chicken Breast'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'calories_per_100g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': '0'}),
            'protein_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'carbs_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'fat_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'fiber_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'sugar_g': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'sodium_mg': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }
        labels = {
            'calories_per_100g': 'Calories (kcal per 100g)',
            'protein_g': 'Protein (g per 100g)',
            'carbs_g': 'Carbohydrates (g per 100g)',
            'fat_g': 'Fat (g per 100g)',
            'fiber_g': 'Fiber (g per 100g)',
            'sugar_g': 'Sugar (g per 100g)',
            'sodium_mg': 'Sodium (mg per 100g)',
        }
