from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<str:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<str:pk>/edit/', views.recipe_update, name='recipe_update'),
    path('recipe/<str:pk>/delete/', views.recipe_delete, name='recipe_delete'),
]
