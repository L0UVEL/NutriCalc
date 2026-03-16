import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Ingredient
from .forms import IngredientForm


# ─── CRUD Views ──────────────────────────────────────────────────────────────

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/list.html'
    context_object_name = 'ingredients'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Ingredient.CATEGORY_CHOICES
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['query'] = self.request.GET.get('q', '')
        ctx['total_count'] = Ingredient.objects.count()
        return ctx


def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'ingredients/detail.html', {'ingredient': ingredient})


def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return redirect('ingredient_detail', pk=ingredient.pk)
    else:
        form = IngredientForm()
    return render(request, 'ingredients/form.html', {'form': form, 'action': 'Add'})


def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_detail', pk=ingredient.pk)
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'ingredients/form.html', {
        'form': form,
        'action': 'Edit',
        'ingredient': ingredient
    })


def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')
    return render(request, 'ingredients/confirm_delete.html', {'ingredient': ingredient})


# ─── REST API Views ───────────────────────────────────────────────────────────

@require_http_methods(["GET"])
def api_ingredient_search(request):
    """GET /api/ingredients/?q=chicken  — returns JSON list for autocomplete"""
    q = request.GET.get('q', '').strip()
    if not q:
        ingredients = Ingredient.objects.all()[:30]
    else:
        ingredients = Ingredient.objects.filter(name__icontains=q)[:20]
    data = [
        {
            'id': ing.pk,
            'name': ing.name,
            'category': ing.get_category_display(),
            'calories_per_100g': ing.calories_per_100g,
            'protein_g': ing.protein_g,
            'carbs_g': ing.carbs_g,
            'fat_g': ing.fat_g,
            'fiber_g': ing.fiber_g,
        }
        for ing in ingredients
    ]
    return JsonResponse({'results': data, 'count': len(data)})


@csrf_exempt
@require_http_methods(["POST"])
def api_calculate_nutrition(request):
    """
    POST /api/calculate/
    Body: {"ingredients": [{"name": "Chicken Breast", "quantity_g": 150}, ...]}
    Returns: total nutrition + per-ingredient breakdown
    """
    try:
        body = json.loads(request.body)
        items = body.get('ingredients', [])
        if not items:
            return JsonResponse({'error': 'No ingredients provided'}, status=400)

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

        # Round totals
        for key in total:
            total[key] = round(total[key], 2)

        return JsonResponse({
            'total': total,
            'breakdown': breakdown,
            'not_found': not_found,
            'ingredient_count': len(breakdown),
        })

    except (json.JSONDecodeError, ValueError, TypeError) as e:
        return JsonResponse({'error': str(e)}, status=400)
