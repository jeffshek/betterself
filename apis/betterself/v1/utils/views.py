from rest_framework.generics import GenericAPIView, ListCreateAPIView


class UserQuerysetFilterMixin(object):
    # for all objects, make sure that we are filtering by the specific user
    def _get_queryset(self):
        # for all objects returned in views, we should always only return what the user i
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class BaseGenericAPIViewV1(GenericAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class BaseGenericListCreateAPIViewV1(ListCreateAPIView, UserQuerysetFilterMixin):
    def get_queryset(self):
        return self._get_queryset()


class ReadOrWriteSerializerChooser(object):
    """
    Mixin to decide read or write serializer class
    """
    def _get_read_or_write_serializer_class(self):
        request_method = self.request.method
        if request_method.lower() in ['list', 'get']:
            return self.read_serializer_class
        else:
            return self.write_serializer_class
