from django.db.models.query import Prefetch
from rest_framework.generics import ListAPIView, ListCreateAPIView

from apis.betterself.v1.supplements.filters import IngredientCompositionFilter, SupplementFilter, \
    UserSupplementStackFilter
from apis.betterself.v1.supplements.serializers import IngredientCompositionReadOnlySerializer, \
    SupplementCreateUpdateSerializer, MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, \
    SupplementReadSerializer, IngredientCompositionCreateSerializer, UserSupplementStackReadSerializer, \
    UserSupplementStackCreateUpdateSerializer, UserSupplementStackCompositionCreateUpdateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement, UserSupplementStack, \
    UserSupplementStackComposition
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


class SupplementsListView(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin):
    read_serializer_class = SupplementReadSerializer
    write_serializer_class = SupplementCreateUpdateSerializer
    update_serializer_class = SupplementCreateUpdateSerializer
    model = Supplement
    filter_class = SupplementFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        # prefetch any compositions that exist to speed this up
        ingredient_compositions_queryset = IngredientComposition.objects.filter(user=self.request.user)
        return self.model.objects.filter(user=self.request.user).prefetch_related(Prefetch('ingredient_compositions',
                                                                                  ingredient_compositions_queryset))


class UserSupplementStackViewSet(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin, UUIDUpdateMixin):
    model = UserSupplementStack
    write_serializer_class = UserSupplementStackCreateUpdateSerializer
    read_serializer_class = UserSupplementStackReadSerializer
    update_serializer_class = UserSupplementStackCreateUpdateSerializer
    filter_class = UserSupplementStackFilter

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).prefetch_related('compositions')


class UserSupplementStackCompositionViewset(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin,
        UUIDUpdateMixin):
    model = UserSupplementStackComposition
    write_serializer_class = UserSupplementStackCompositionCreateUpdateSerializer
