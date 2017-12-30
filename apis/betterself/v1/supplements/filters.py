import django_filters
from django_filters.rest_framework import FilterSet

from supplements.models import IngredientComposition, Supplement, UserSupplementStack, UserSupplementStackComposition


class IngredientCompositionFilter(FilterSet):
    ingredient_uuid = django_filters.UUIDFilter(name='ingredient__uuid')
    measurement_uuid = django_filters.UUIDFilter(name='measurement__uuid')

    class Meta:
        model = IngredientComposition
        fields = ['ingredient_uuid', 'quantity', 'measurement_uuid', 'uuid']


class SupplementFilter(FilterSet):
    # TODO - This doesn't support multiple compositions very well, but we'll worry about that later
    # Right now, only filters one
    ingredient_compositions_uuids = django_filters.CharFilter(name='ingredient_compositions__uuid')

    class Meta:
        model = Supplement
        fields = ['ingredient_compositions_uuids', 'name', 'uuid']


class UserSupplementStackFilter(FilterSet):
    # TODO - This doesn't support multiple supplements very well, but we'll worry about that later
    # Right now, only filters one
    supplement_uuids = django_filters.CharFilter(name='supplements__uuid')

    class Meta:
        model = UserSupplementStack
        fields = ['supplement_uuids', 'name', 'uuid']


class UserSupplementStackCompositionFilter(FilterSet):
    class Meta:
        model = UserSupplementStackComposition
        fields = ['uuid', 'quantity']
