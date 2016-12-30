from rest_framework.generics import ListAPIView

from apis.betterself.v1.supplements.serializers import IngredientCompositionReadOnlySerializer, \
    SupplementCreateSerializer, MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, \
    SupplementReadOnlySerializer, IngredientCompositionCreateSerializer
from apis.betterself.v1.utils.views import UserQuerysetFilterMixin, BaseGenericListCreateAPIViewV1
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement
from vendors.models import Vendor

"""
These inherited models such as BaseGenericListCreateAPIViewV1 contain a override to get_queryset
so that users won't have access to models that are not the default or don't belong to them!
"""


class VendorView(BaseGenericListCreateAPIViewV1):
    serializer_class = VendorSerializer
    model = Vendor
    filter_fields = ('name',)


class MeasurementView(ListAPIView):
    # Users are not allowed to create measurements, only can choose
    # whatever is on the default
    serializer_class = MeasurementReadOnlySerializer
    model = Measurement

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            queryset = self.model.objects.filter(name=name)
        else:
            queryset = self.model.objects.all()

        return queryset


class IngredientView(BaseGenericListCreateAPIViewV1):
    serializer_class = IngredientSerializer
    model = Ingredient


class IngredientCompositionView(BaseGenericListCreateAPIViewV1):
    read_serializer_class = IngredientCompositionReadOnlySerializer
    write_serializer_class = IngredientCompositionCreateSerializer
    model = IngredientComposition

    def get_serializer_class(self):
        request_method = self.request.method
        if request_method.lower() in ['list', 'get']:
            return self.read_serializer_class
        else:
            return self.write_serializer_class


class SupplementView(BaseGenericListCreateAPIViewV1, UserQuerysetFilterMixin):
    read_serializer_class = SupplementReadOnlySerializer
    write_serializer_class = SupplementCreateSerializer
    model = Supplement

    def get_serializer_class(self):
        request_method = self.request.method
        if request_method.lower() in ['list', 'get']:
            return self.read_serializer_class
        else:
            return self.write_serializer_class
