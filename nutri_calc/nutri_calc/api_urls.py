from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ingredients.api_views import IngredientViewSet, NutritionCalculationView
from recipes.api_views import RecipeViewSet

# DefaultRouter generates the API root automatically.
# Setting trailing_slash=False as per requirements.
router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ingredients': reverse('ingredients-list', request=request, format=format),
        'recipes': reverse('recipes-list', request=request, format=format),
        'nutrition-calculations': reverse('api-nutrition-calculations', request=request, format=format),
    })

urlpatterns = [
    # Custom API root to include both router views and manual views
    path('', api_root, name='api-root'),
    # Router covers /api/ingredients and /api/recipes
    path('', include(router.urls)),
    # Specific APIView for calculations
    path('nutrition-calculations', NutritionCalculationView.as_view(), name='api-nutrition-calculations'),
]
