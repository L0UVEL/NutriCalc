from rest_framework import viewsets, views, status
from rest_framework.response import Response
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if category:
            qs = qs.filter(category=category)
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

class NutritionCalculationView(views.APIView):
    def post(self, request, *args, **kwargs):
        items = request.data.get('ingredients', [])
        if not items:
            return Response({'error': 'No ingredients provided'}, status=status.HTTP_400_BAD_REQUEST)

        total = {'calories': 0.0, 'protein_g': 0.0, 'carbs_g': 0.0,
                 'fat_g': 0.0, 'fiber_g': 0.0, 'sugar_g': 0.0, 'sodium_mg': 0.0}
        breakdown = []
        not_found = []

        for item in items:
            name = item.get('name', '').strip()
            try:
                qty = float(item.get('quantity_g', 0))
            except (ValueError, TypeError):
                qty = 0.0
            
            try:
                ing = Ingredient.objects.get(name__iexact=name)
                factor = qty / 100.0
                row = {
                    'name': ing.name,
                    'quantity_g': qty,
                    # Provide original category machine name
                    'category': ing.category,
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

        return Response({
            'total': total,
            'breakdown': breakdown,
            'not_found': not_found,
            'ingredient_count': len(breakdown),
        })
