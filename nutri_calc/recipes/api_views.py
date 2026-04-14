from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.models import Recipe, RecipeIngredient
from recipes.serializers import RecipeSerializer, RecipeIngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    @action(detail=True, methods=['get', 'post'])
    def ingredients(self, request, pk=None):
        recipe = self.get_object()
        
        if request.method == 'GET':
            qs = recipe.recipe_ingredients.all()
            serializer = RecipeIngredientSerializer(qs, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            # Create a mutable copy if request.data is immutable
            data = request.data.copy() if hasattr(request.data, 'copy') else request.data
            serializer = RecipeIngredientSerializer(data=data)
            if serializer.is_valid():
                serializer.save(recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
