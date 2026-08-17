from django.contrib import admin
from django.apps import apps
from .models import *

# Automatically register all models in the app
app_models = apps.get_app_config('core').get_models()

for model in app_models:
    admin.site.register(model)