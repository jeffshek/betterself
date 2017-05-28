from rest_framework.generics import ListAPIView, ListCreateAPIView

from apis.betterself.v1.supplements.filters import IngredientCompositionFilter, SupplementFilter
from apis.betterself.v1.supplements.serializers import IngredientCompositionReadOnlySerializer, \
    SupplementCreateSerializer, MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, \
    SupplementReadOnlySerializer, IngredientCompositionCreateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement
from vendors.models import Vendor

"""
These inherited models such as BaseGenericListCreateAPIViewV1 contain a override to get_queryset
so that users won't have access to models that are not the default or don't belong to them!
"""


class VendorView(ListCreateAPIView):
    serializer_class = VendorSerializer
    model = Vendor
    filter_fields = ('name', 'uuid')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class MeasurementView(ListAPIView):
    # Users are not allowed to create measurements, only can choose
    # whatever is on the default
    serializer_class = MeasurementReadOnlySerializer
    model = Measurement
    filter_fields = ('name', 'uuid')
    queryset = Measurement.objects.all()


class IngredientView(ListCreateAPIView):
    serializer_class = IngredientSerializer
    model = Ingredient
    filter_fields = ('name', 'half_life_minutes', 'uuid')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class IngredientCompositionView(ListCreateAPIView, ReadOrWriteSerializerChooser):
    read_serializer_class = IngredientCompositionReadOnlySerializer
    write_serializer_class = IngredientCompositionCreateSerializer
    model = IngredientComposition
    filter_class = IngredientCompositionFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class SupplementView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    read_serializer_class = SupplementReadOnlySerializer
    write_serializer_class = SupplementCreateSerializer
    model = Supplement
    filter_class = SupplementFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# TODO - Add delete tests
