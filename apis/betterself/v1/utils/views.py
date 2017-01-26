from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListCreateAPIView


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
        default_user = get_user_model().objects.get(username='default')
        queryset = self.model.objects.filter(Q(user=self.request.user) | Q(user=default_user))
        return queryset


class BaseGenericAPIViewV1(GenericAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class BaseGenericListCreateAPIViewV1(ListCreateAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class ReadOrWriteViewInterfaceV1(object):
    """
    Mixin to decide read or write serializer class
    """
    def _get_read_or_write_serializer_class(self):
        request_method = self.request.method
        if request_method.lower() in ['list', 'get']:
            return self.read_serializer_class
        else:
            return self.write_serializer_class
