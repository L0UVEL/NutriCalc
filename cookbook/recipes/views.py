import requests
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientFormSet


INGREDIENT_DB_URL = getattr(settings, 'INGREDIENT_DB_URL', 'http://localhost:8000')


# ─── AI Guide ────────────────────────────────────────────────────────────────

def generate_ai_tips(nutrition, ingredients):
    """Rule-based AI nutritional guide that returns personalized tips and warnings."""
    tips = []
    warnings = []
    suggestions = []

    cal = nutrition.get('calories', 0)
    protein = nutrition.get('protein_g', 0)
    carbs = nutrition.get('carbs_g', 0)
    fat = nutrition.get('fat_g', 0)
    fiber = nutrition.get('fiber_g', 0)
    sodium = nutrition.get('sodium_mg', 0)
    count = nutrition.get('ingredient_count', 1) or 1

    # Calorie assessment
    if cal > 800:
        warnings.append("This recipe is high in calories. Consider reducing portion size or using lower-calorie ingredient alternatives.")
    elif cal < 200:
        tips.append("This is a light recipe! Great for a snack or side dish. Pair it with a protein source for a complete meal.")
    else:
        tips.append("This recipe has a balanced calorie count — suitable for a main course meal.")

    # Protein assessment
    if protein < 15:
        suggestions.append("Protein is low. Try adding chicken breast, lentils, Greek yogurt, eggs, or tofu to boost it.")
    elif protein > 40:
        tips.append("Excellent protein content! This recipe supports muscle building and satiety.")
    else:
        tips.append("Good protein level — your body will thank you!")

    # Carb assessment
    if carbs > 80:
        warnings.append("High in carbohydrates. If you're watching your carb intake, consider substituting with cauliflower rice or zucchini noodles.")
    elif carbs < 15:
        tips.append("Low-carb recipe! Perfect for keto or low-glycemic diets.")

    # Fat assessment
    if fat > 50:
        warnings.append("High fat content detected. Consider using olive oil sparingly or switching to low-fat dairy options.")
    elif fat < 5:
        tips.append("Very low fat — this is a lean recipe, great for heart health!")

    # Fiber assessment
    if fiber < 3:
        suggestions.append("Add fiber-rich ingredients like broccoli, oats, black beans, or chia seeds to improve digestive health.")
    elif fiber > 10:
        tips.append("High fiber! Great for digestive health and keeping you full longer.")

    # Sodium assessment
    if sodium > 1500:
        warnings.append("Sodium is very high. Reduce soy sauce, processed meats, or canned goods. Look for low-sodium alternatives.")
    elif sodium > 800:
        warnings.append("Sodium is moderately high. Consider using herbs and spices instead of salt for flavor.")

    # Macro balance tip
    total_macro = protein + carbs + fat
    if total_macro > 0:
        p_pct = (protein / total_macro) * 100
        c_pct = (carbs / total_macro) * 100
        f_pct = (fat / total_macro) * 100
        if p_pct >= 30 and c_pct >= 30 and f_pct <= 35:
            tips.append("Well-balanced macros (protein/carbs/fat ratio)! This recipe follows a healthy eating pattern.")

    # Ingredient count tips
    if count <= 3:
        tips.append("Simple recipe with few ingredients! Great for meal prep and quick cooking.")
    elif count >= 8:
        tips.append("Complex recipe with many ingredients — rich in variety of nutrients!")

    # Cooking suggestions based on ingredients
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
    """Returns a 0–100 health score with label."""
    score = 50  # baseline
    # Protein boost
    if protein >= 20: score += 15
    elif protein >= 10: score += 8
    # Fiber boost
    if fiber >= 8: score += 10
    elif fiber >= 4: score += 5
    # Calorie penalty
    if cal > 900: score -= 15
    elif cal > 600: score -= 7
    # Fat penalty
    if fat > 50: score -= 10
    elif fat > 30: score -= 5
    # Sodium penalty
    if sodium > 1500: score -= 15
    elif sodium > 800: score -= 7
    # Carb penalty
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
    api_error = None

    if ingredients:
        payload = {
            'ingredients': [
                {'name': ri.ingredient_name, 'quantity_g': ri.quantity_g}
                for ri in ingredients
            ]
        }
        try:
            resp = requests.post(
                f'{INGREDIENT_DB_URL}/api/calculate/',
                json=payload,
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                nutrition = data
                ing_names = [ri.ingredient_name for ri in ingredients]
                ai_guide = generate_ai_tips(data['total'], ing_names)
                nutrition['ingredient_count'] = data.get('ingredient_count', len(ingredients))
            else:
                api_error = f"App A returned status {resp.status_code}"
        except requests.exceptions.ConnectionError:
            api_error = "Cannot connect to the Ingredient DB (App A). Make sure it is running on port 8000."
        except requests.exceptions.Timeout:
            api_error = "Request to Ingredient DB timed out. Please try again."

    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'nutrition': nutrition,
        'ai_guide': ai_guide,
        'api_error': api_error,
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

    # Load ingredient suggestions from App A for autocomplete
    ingredient_suggestions = []
    try:
        resp = requests.get(f'{INGREDIENT_DB_URL}/api/ingredients/', timeout=3)
        if resp.status_code == 200:
            ingredient_suggestions = [i['name'] for i in resp.json().get('results', [])]
    except Exception:
        pass

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

    ingredient_suggestions = []
    try:
        resp = requests.get(f'{INGREDIENT_DB_URL}/api/ingredients/', timeout=3)
        if resp.status_code == 200:
            ingredient_suggestions = [i['name'] for i in resp.json().get('results', [])]
    except Exception:
        pass

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


# ─── AJAX Ingredient Search (proxies to App A) ───────────────────────────────

def api_ingredient_search_proxy(request):
    q = request.GET.get('q', '')
    try:
        resp = requests.get(f'{INGREDIENT_DB_URL}/api/ingredients/?q={q}', timeout=3)
        return JsonResponse(resp.json())
    except Exception as e:
        return JsonResponse({'results': [], 'error': str(e)})
