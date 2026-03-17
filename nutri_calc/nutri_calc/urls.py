from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # App A — Ingredient DB (root URLs)
    path('', include('ingredients.urls')),
    # App B — Cookbook (prefixed with /cookbook/)
    path('cookbook/', include('recipes.urls')),
]
