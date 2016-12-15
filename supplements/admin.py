from django.contrib import admin

from supplements.models import Measurement, Ingredient, IngredientComposition, Supplement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_liquid')

    class Meta:
        model = Measurement


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'half_life_minutes')
    search_fields = ('user__username', 'name')

    class Meta:
        model = Ingredient


@admin.register(IngredientComposition)
class IngredientCompositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient_name', 'measurement', 'quantity')

    class Meta:
        model = IngredientComposition

    @staticmethod
    def ingredient_name(instance):
        return instance.ingredient.name


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'ingredient_composition_display', 'vendor')

    class Meta:
        model = Supplement

    @staticmethod
    def ingredient_composition_display(instance):
        ingredient_composition = instance.ingredient_compositions.all()

        if ingredient_composition.exists():
            return ingredient_composition.values_list('ingredient__name', flat=True)
