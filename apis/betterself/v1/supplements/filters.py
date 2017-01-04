import django_filters
from django_filters.rest_framework import FilterSet

from supplements.models import IngredientComposition


class IngredientCompositionFilter(FilterSet):
    ingredient_uuid = django_filters.CharFilter(name='ingredient__uuid')
    measurement_uuid = django_filters.CharFilter(name='measurement__uuid')

    class Meta:
        model = IngredientComposition
        fields = ['ingredient_uuid', 'quantity', 'measurement_uuid']
