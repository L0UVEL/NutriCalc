from django.urls import path
from ingredients import views

urlpatterns = [
    # CRUD
    path('', views.IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/<str:pk>/', views.ingredient_detail, name='ingredient_detail'),
    path('ingredient/add/', views.ingredient_create, name='ingredient_create'),
    path('ingredient/<str:pk>/edit/', views.ingredient_update, name='ingredient_update'),
    path('ingredient/<str:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),
]
