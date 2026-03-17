import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from ingredients.models import Ingredient
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientFormSet


# ─── Nutrition calculation (direct import from ingredients app — no HTTP) ─────

def _calculate_nutrition_direct(items):
    """
    Calculate nutrition directly from the Ingredient model.
    items: list of dicts: [{'name': 'Chicken Breast', 'quantity_g': 150}, ...]
    Returns the same structure as the /api/calculate/ JSON response.
    """
    total = {'calories': 0.0, 'protein_g': 0.0, 'carbs_g': 0.0,
             'fat_g': 0.0, 'fiber_g': 0.0, 'sugar_g': 0.0, 'sodium_mg': 0.0}
    breakdown = []
    not_found = []

    for item in items:
        name = item.get('name', '').strip()
        qty = float(item.get('quantity_g', 0))
        try:
            ing = Ingredient.objects.get(name__iexact=name)
            factor = qty / 100.0
            row = {
                'name': ing.name,
                'quantity_g': qty,
                'category': ing.get_category_display(),
                'calories': round(ing.calories_per_100g * factor, 2),
                'protein_g': round(ing.protein_g * factor, 2),
                'carbs_g': round(ing.carbs_g * factor, 2),
                'fat_g': round(ing.fat_g * factor, 2),
                'fiber_g': round(ing.fiber_g * factor, 2),
                'sugar_g': round(ing.sugar_g * factor, 2),
                'sodium_mg': round(ing.sodium_mg * factor, 2),
            }
            breakdown.append(row)
            for key in total:
                total[key] += row[key]
        except Ingredient.DoesNotExist:
            not_found.append(name)

    for key in total:
        total[key] = round(total[key], 2)

    return {
        'total': total,
        'breakdown': breakdown,
        'not_found': not_found,
        'ingredient_count': len(breakdown),
    }


# ─── AI Guide ────────────────────────────────────────────────────────────────

def generate_ai_tips(nutrition, ingredients):
    """Rule-based AI nutritional guide."""
    tips, warnings, suggestions = [], [], []

    cal = nutrition.get('calories', 0)
    protein = nutrition.get('protein_g', 0)
    carbs = nutrition.get('carbs_g', 0)
    fat = nutrition.get('fat_g', 0)
    fiber = nutrition.get('fiber_g', 0)
    sodium = nutrition.get('sodium_mg', 0)
    count = nutrition.get('ingredient_count', 1) or 1

    if cal > 800:
        warnings.append("This recipe is high in calories. Consider reducing portion size or using lower-calorie alternatives.")
    elif cal < 200:
        tips.append("This is a light recipe! Great for a snack. Pair it with a protein source for a complete meal.")
    else:
        tips.append("This recipe has a balanced calorie count — suitable for a main course meal.")

    if protein < 15:
        suggestions.append("Protein is low. Try adding chicken breast, lentils, Greek yogurt, eggs, or tofu to boost it.")
    elif protein > 40:
        tips.append("Excellent protein content! This recipe supports muscle building and satiety.")
    else:
        tips.append("Good protein level!")

    if carbs > 80:
        warnings.append("High in carbohydrates. Consider substituting with cauliflower rice or zucchini noodles.")
    elif carbs < 15:
        tips.append("Low-carb recipe! Perfect for keto or low-glycemic diets.")

    if fat > 50:
        warnings.append("High fat content. Consider using olive oil sparingly or switching to low-fat dairy options.")
    elif fat < 5:
        tips.append("Very low fat — a lean recipe, great for heart health!")

    if fiber < 3:
        suggestions.append("Add fiber-rich ingredients like broccoli, oats, black beans, or chia seeds.")
    elif fiber > 10:
        tips.append("High fiber! Great for digestive health and keeping you full longer.")

    if sodium > 1500:
        warnings.append("Sodium is very high. Reduce soy sauce, processed meats, or canned goods.")
    elif sodium > 800:
        warnings.append("Sodium is moderately high. Consider using herbs and spices instead of salt.")

    total_macro = protein + carbs + fat
    if total_macro > 0:
        p_pct = (protein / total_macro) * 100
        c_pct = (carbs / total_macro) * 100
        f_pct = (fat / total_macro) * 100
        if p_pct >= 30 and c_pct >= 30 and f_pct <= 35:
            tips.append("Well-balanced macros! This recipe follows a healthy eating pattern.")

    if count <= 3:
        tips.append("Simple recipe with few ingredients! Great for meal prep.")
    elif count >= 8:
        tips.append("Complex recipe with many ingredients — rich in nutritional variety!")

    ing_names = [i.lower() for i in ingredients]
    if any('oil' in n or 'butter' in n for n in ing_names):
        suggestions.append("Tip: Use non-stick cookware to minimize the amount of oil or butter needed.")
    if any('sugar' in n or 'honey' in n for n in ing_names):
        suggestions.append("Tip: Try reducing sugar by 20% — most recipes taste just as good with less!")
    if any('salt' in n or 'sodium' in n or 'soy' in n for n in ing_names):
        suggestions.append("Tip: Season at the end of cooking to use less salt while achieving the same flavor.")

    return {
        'tips': tips,
        'warnings': warnings,
        'suggestions': suggestions,
        'score': _calculate_health_score(cal, protein, carbs, fat, fiber, sodium),
    }


def _calculate_health_score(cal, protein, carbs, fat, fiber, sodium):
    score = 50
    if protein >= 20: score += 15
    elif protein >= 10: score += 8
    if fiber >= 8: score += 10
    elif fiber >= 4: score += 5
    if cal > 900: score -= 15
    elif cal > 600: score -= 7
    if fat > 50: score -= 10
    elif fat > 30: score -= 5
    if sodium > 1500: score -= 15
    elif sodium > 800: score -= 7
    if carbs > 80: score -= 8
    score = max(0, min(100, score))
    if score >= 75: label = 'Excellent'
    elif score >= 55: label = 'Good'
    elif score >= 35: label = 'Fair'
    else: label = 'Poor'
    return {'value': score, 'label': label}


# ─── CRUD Views ──────────────────────────────────────────────────────────────

def recipe_list(request):
    recipes = Recipe.objects.prefetch_related('recipe_ingredients').all()
    q = request.GET.get('q', '').strip()
    if q:
        recipes = recipes.filter(name__icontains=q)
    return render(request, 'recipes/list.html', {
        'recipes': recipes,
        'query': q,
        'total': Recipe.objects.count(),
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipe_ingredients.all()
    nutrition = None
    ai_guide = None

    if ingredients:
        payload = [
            {'name': ri.ingredient_name, 'quantity_g': ri.quantity_g}
            for ri in ingredients
        ]
        nutrition = _calculate_nutrition_direct(payload)
        ing_names = [ri.ingredient_name for ri in ingredients]
        ai_guide = generate_ai_tips(nutrition['total'], ing_names)

    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'nutrition': nutrition,
        'ai_guide': ai_guide,
    })


def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            instances = formset.save(commit=False)
            for inst in instances:
                inst.recipe = recipe
                inst.save()
            messages.success(request, f'Recipe "{recipe.name}" created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    # Load ingredient names directly from DB for autocomplete
    ingredient_suggestions = list(
        Ingredient.objects.values_list('name', flat=True).order_by('name')
    )
    return render(request, 'recipes/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Create',
        'ingredient_suggestions': json.dumps(ingredient_suggestions),
    })


def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Recipe "{recipe.name}" updated!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    ingredient_suggestions = list(
        Ingredient.objects.values_list('name', flat=True).order_by('name')
    )
    return render(request, 'recipes/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Edit',
        'recipe': recipe,
        'ingredient_suggestions': json.dumps(ingredient_suggestions),
    })


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        name = recipe.name
        recipe.delete()
        messages.success(request, f'Recipe "{name}" deleted.')
        return redirect('recipe_list')
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})


# ─── Ingredient Search API (for external use / AJAX) ────────────────────────

def api_ingredient_search(request):
    """GET /api/ingredients/?q=chicken"""
    q = request.GET.get('q', '').strip()
    qs = Ingredient.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    data = [
        {
            'id': ing.pk,
            'name': ing.name,
            'category': ing.get_category_display(),
            'calories_per_100g': ing.calories_per_100g,
        }
        for ing in qs[:20]
    ]
    return JsonResponse({'results': data})
