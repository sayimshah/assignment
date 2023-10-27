from django.contrib import admin
from django.apps import apps

# Register your models here.
def register_all_models(admin_site, core):
    app_models = apps.get_app_config(core).get_models()
    for model in app_models:
        admin_site.register(model)

# Replace 'your_app_name' with the name of your Django app.
register_all_models(admin.site, 'core')