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
        queryset = self.model.objects.filter(Q(user=self.request.user) | Q(user=None))
        return queryset


class BaseGenericAPIViewV1(GenericAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class BaseGenericListCreateAPIViewV1(ListCreateAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()
