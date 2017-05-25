from django.http.response import Http404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from apis.betterself.v1.supplements.filters import IngredientCompositionFilter, SupplementFilter
from apis.betterself.v1.supplements.serializers import IngredientCompositionReadOnlySerializer, \
    SupplementCreateSerializer, MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, \
    SupplementReadOnlySerializer, IngredientCompositionCreateSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1, ReadOrWriteSerializerChooser
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


class IngredientCompositionView(BaseGenericListCreateAPIViewV1, ReadOrWriteSerializerChooser):
    read_serializer_class = IngredientCompositionReadOnlySerializer
    write_serializer_class = IngredientCompositionCreateSerializer
    model = IngredientComposition
    filter_class = IngredientCompositionFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()


class SupplementView(BaseGenericListCreateAPIViewV1, ReadOrWriteSerializerChooser, RetrieveUpdateDestroyAPIView):
    read_serializer_class = SupplementReadOnlySerializer
    write_serializer_class = SupplementCreateSerializer
    model = Supplement
    filter_class = SupplementFilter

    def get_queryset(self):
        return super().get_queryset().prefetch_related('ingredient_compositions')

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def destroy(self, request, *args, **kwargs):
        try:
            uuid = request.data['uuid']
        except KeyError:
            raise Http404

        filter_params = {
            'uuid': uuid,
            'user': request.user
        }

        object = get_object_or_404(self.model, **filter_params)
        object.delete()
        return Response(status=204)
