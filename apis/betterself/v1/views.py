from rest_framework.generics import GenericAPIView
from supplements.models import Ingredient, IngredientComposition, MeasurementUnit, SupplementProduct


class BaseGenericAPIViewV1(GenericAPIView):
    def get_queryset(self):

        return


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
