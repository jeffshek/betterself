from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from apis.betterself.v1.supplements.filters import IngredientCompositionFilter, SupplementFilter
from apis.betterself.v1.supplements.serializers import IngredientCompositionReadOnlySerializer, \
    SupplementCreateSerializer, MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, \
    SupplementReadOnlySerializer, IngredientCompositionCreateSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement
from vendors.models import Vendor

"""
These inherited models such as BaseGenericListCreateAPIViewV1 contain a override to get_queryset
so that users won't have access to models that are not the default or don't belong to them!
"""


class VendorView(BaseGenericListCreateAPIViewV1):
    serializer_class = VendorSerializer
    model = Vendor
    filter_fields = ('name', 'uuid')


class MeasurementView(ListAPIView):
    # Users are not allowed to create measurements, only can choose
    # whatever is on the default
    serializer_class = MeasurementReadOnlySerializer
    model = Measurement
    filter_fields = ('name', 'uuid')
    queryset = Measurement.objects.all()


class IngredientView(BaseGenericListCreateAPIViewV1):
    serializer_class = IngredientSerializer
    model = Ingredient
    filter_fields = ('name', 'half_life_minutes', 'uuid')


class IngredientCompositionView(BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1):
    read_serializer_class = IngredientCompositionReadOnlySerializer
    write_serializer_class = IngredientCompositionCreateSerializer
    model = IngredientComposition
    filter_class = IngredientCompositionFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()


class SupplementView(BaseGenericListCreateAPIViewV1, ReadOrWriteViewInterfaceV1, RetrieveUpdateDestroyAPIView):
    read_serializer_class = SupplementReadOnlySerializer
    write_serializer_class = SupplementCreateSerializer
    model = Supplement
    filter_class = SupplementFilter

    def get_queryset(self):
        return super().get_queryset().prefetch_related('ingredient_compositions')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def delete(self, request, *args, **kwargs):
        data = self.model.objects.get(uuid=request.data['uuid'], user=self.request.user)
        data.delete()
        return Response({}, status=202)
