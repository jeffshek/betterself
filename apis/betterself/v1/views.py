from rest_framework.generics import GenericAPIView
from django.db.models import Q

from supplements.models import Ingredient, IngredientComposition, MeasurementUnit, SupplementProduct


class BaseGenericAPIViewV1(GenericAPIView):
    model = None

    def get_queryset(self):
        # for all objects returned, a user should only see either
        # objects that don't belong to a user or objects owned by a
        # specific user
        queryset = self.model.filter(Q(user=self.request.user) | Q(user=None))
        return queryset


class IngredientView(BaseGenericAPIViewV1):
    serializer_class = None
    model = Ingredient


class MeasurementUnitView(BaseGenericAPIViewV1):
    serializer_class = None
    model = MeasurementUnit


class IngredientCompositionView(BaseGenericAPIViewV1):
    serializer_class = None
    model = IngredientComposition


class SupplementProductView(BaseGenericAPIViewV1):
    serializer_class = None
    model = SupplementProduct
