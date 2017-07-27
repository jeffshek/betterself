from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.rescuetime.v1.serializers import UpdateRescueTimeAPISerializer


class UpdateRescueTimeAPIView(APIView):
    def post(self, request):
        # user = request.user
        data = request.data

        try:
            initial_data = {
                'rescuetime_api_key': data['rescuetime_api_key'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
            }
        except (MultiValueDictKeyError, KeyError) as exc:
            return Response('Missing POST parameters {}'.format(exc), status=400)

        serializer = UpdateRescueTimeAPISerializer(data=initial_data)
        if not serializer.is_valid():
            return Response('{}'.format(serializer.errors), status=400)

        return Response(status=202)
