from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


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


class UUIDDeleteMixin(object):
    """
    Mixin for API Views to allow deleting of objects
    """

    def delete(self, request, *args, **kwargs):
        try:
            uuid = request.data['uuid']
        except KeyError:
            raise Http404

        filter_params = {
            'uuid': uuid,
            'user': request.user
        }

        get_object_or_404(self.model, **filter_params).delete()
        return Response(status=204)


class UUIDUpdateMixin(object):
    """
    Mixin for API Views to allow updating of objects
    """

    def put(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        try:
            uuid = data['uuid']
        except KeyError:
            raise Http404

        instance = get_object_or_404(self.model, user=user, uuid=uuid)
        serializer = self.update_serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            Response('Invalid Data Submitted {}'.format(data), status=400)

        return Response(serializer.data)
