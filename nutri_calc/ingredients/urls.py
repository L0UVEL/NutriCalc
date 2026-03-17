from django.urls import path
from . import views

urlpatterns = [
    # CRUD
    path('', views.IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/<int:pk>/', views.ingredient_detail, name='ingredient_detail'),
    path('ingredient/add/', views.ingredient_create, name='ingredient_create'),
    path('ingredient/<int:pk>/edit/', views.ingredient_update, name='ingredient_update'),
    path('ingredient/<int:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),
    # REST API
    path('api/ingredients/', views.api_ingredient_search, name='api_ingredients'),
    path('api/calculate/', views.api_calculate_nutrition, name='api_calculate'),
]
