from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.rescuetime.tasks import import_user_history_via_api
from apis.rescuetime.v1.serializers import RescueTimeAPIRequestSerializer


class UpdateRescueTimeAPIView(APIView):
    # don't slam rescuetime's servers, so you won't get banned
    throttle_scope = 'rescuetime-api-sync'

    def post(self, request):
        user = request.user
        data = request.data

        try:
            initial_data = {
                'rescuetime_api_key': data['rescuetime_api_key'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
            }
        except (MultiValueDictKeyError, KeyError) as exc:
            return Response('Missing POST parameters {}'.format(exc), status=400)

        serializer = RescueTimeAPIRequestSerializer(data=initial_data)
        if not serializer.is_valid():
            return Response('{}'.format(serializer.errors), status=400)

        # send the job off to celery so it's an async task
        import_user_history_via_api.delay(user=user, **serializer.validated_data)

        return Response(status=202)
