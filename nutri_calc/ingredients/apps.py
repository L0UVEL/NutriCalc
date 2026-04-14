from django.apps import AppConfig


class IngredientsConfig(AppConfig):
    # default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingredients'
