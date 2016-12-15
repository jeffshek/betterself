from django.contrib import admin

from supplements.models import Measurement, Ingredient, IngredientComposition, Supplement

# TODO - Create customized admin views
admin.site.register(Measurement)
admin.site.register(Ingredient)
admin.site.register(IngredientComposition)
admin.site.register(Supplement)
