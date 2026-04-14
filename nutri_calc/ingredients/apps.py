from django.apps import AppConfig


class IngredientsConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'ingredients'
