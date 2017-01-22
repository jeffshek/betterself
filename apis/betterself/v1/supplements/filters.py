import django_filters
from django_filters.rest_framework import FilterSet

from supplements.models import IngredientComposition, Supplement


class IngredientCompositionFilter(FilterSet):
    # this is really ghetto please fix this, look into just using UUID
    ingredient_uuid = django_filters.CharFilter(name='ingredient__uuid')
    measurement_uuid = django_filters.CharFilter(name='measurement__uuid')
    quantity = django_filters.NumberFilter(name='quantity')
    uuid = django_filters.UUIDFilter(name='uuid')

    class Meta:
        model = IngredientComposition
        fields = ['ingredient_uuid', 'quantity', 'measurement_uuid', 'uuid']


class SupplementFilter(FilterSet):
    # this is really ghetto please fix this
    # also please add a test for the love of god
    ingredient_compositions_uuids = django_filters.CharFilter(
        name='ingredient_compositions__uuid', lookup_expr='contains')

    class Meta:
        model = Supplement
        fields = ['ingredient_compositions_uuids', 'name', 'vendor']
