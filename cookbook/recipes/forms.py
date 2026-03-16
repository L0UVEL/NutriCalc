from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'servings']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Grilled Chicken Salad'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Brief description...'}),
            'instructions': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Step-by-step cooking instructions...'}),
            'servings': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_name', 'quantity_g']
        widgets = {
            'ingredient_name': forms.TextInput(attrs={
                'class': 'form-input ing-name-input',
                'placeholder': 'e.g. Chicken Breast (cooked)',
                'autocomplete': 'off',
            }),
            'quantity_g': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'grams',
                'min': '0.1',
                'step': '0.1',
            }),
        }
        labels = {
            'ingredient_name': 'Ingredient',
            'quantity_g': 'Quantity (g)',
        }


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
