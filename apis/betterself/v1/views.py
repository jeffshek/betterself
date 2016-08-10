from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView

from apis.betterself.v1.serializers import IngredientCompositionReadOnlySerializer, SupplementCreateSerializer, \
    MeasurementReadOnlySerializer, IngredientSerializer, VendorSerializer, SupplementReadOnlySerializer, \
    IngredientCompositionCreateSerializer
from supplements.models import Ingredient, IngredientComposition, Measurement, Supplement
from vendors.models import Vendor


class UserQuerysetFilterMixin(object):
    # this is kind of weird, but because most of the resources need to have
    # a ownership principle (access to objects with no owner or owned by specific user)
    # have a mixin that will filter everything - hopefully preventing situations
    # where someone has access to data they shouldn't
    # ignore MRO / duped issues by using a template style
    def _get_queryset(self):
        # for all objects returned, a user should only see either
        # objects that don't belong to a user or objects owned by a
        # specific user
        queryset = self.model.objects.filter(Q(user=self.request.user) | Q(user=None))
        return queryset


class BaseGenericAPIViewV1(GenericAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class BaseGenericListCreateAPIViewV1(ListCreateAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class VendorView(BaseGenericListCreateAPIViewV1):
    serializer_class = VendorSerializer
    model = Vendor


class MeasurementView(ListAPIView):
    # TD - Switch to proxy asap
    serializer_class = MeasurementReadOnlySerializer
    model = Measurement

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            queryset = self.model.objects.filter(name__iexact=name)
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


class EventView(BaseGenericListCreateAPIViewV1, UserQuerysetFilterMixin):
    pass
