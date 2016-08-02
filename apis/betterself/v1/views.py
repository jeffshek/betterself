from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListCreateAPIView

from apis.betterself.v1.serializers import IngredientCompositionSerializer, SupplementCreateSerializer, \
    MeasurementSerializer, IngredientSerializer, VendorSerializer, SupplementReadSerializer
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

# Have generic views that override get_queryset


class BaseGenericAPIViewV1(GenericAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class BaseGenericListCreateAPIViewV1(ListCreateAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class VendorView(BaseGenericListCreateAPIViewV1):
    serializer_class = VendorSerializer
    model = Vendor


class IngredientView(BaseGenericAPIViewV1):
    serializer_class = IngredientSerializer
    model = Ingredient


class MeasurementView(BaseGenericAPIViewV1):
    serializer_class = MeasurementSerializer
    model = Measurement


class IngredientCompositionView(BaseGenericAPIViewV1):
    serializer_class = IngredientCompositionSerializer
    model = IngredientComposition


class SupplementView(BaseGenericListCreateAPIViewV1, UserQuerysetFilterMixin):
    # this can probably be named better
    read_serializer_class = SupplementReadSerializer
    write_serializer_class = SupplementCreateSerializer
    model = Supplement

    def get_serializer_class(self):
        request_method = self.request.method
        if request_method.lower() in ['list', 'get']:
            return self.read_serializer_class
        else:
            return self.write_serializer_class
