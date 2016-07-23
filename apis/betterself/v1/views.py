from django.http import HttpResponse
from rest_framework.generics import GenericAPIView


class APIv1Views(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Base Text", content_type="text/plain")
