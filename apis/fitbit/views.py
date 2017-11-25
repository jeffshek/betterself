from django.http.response import Http404
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apis.fitbit import utils
from apis.fitbit.models import UserFitbit
from apis.fitbit.serializers import FitbitAPIRequestSerializer
from apis.fitbit.tasks import import_user_fitbit_history_via_api
from apis.fitbit.utils import is_integrated


class FitbitLoginView(APIView):
    def get(self, request):
        next_url = request.GET.get('next', None)
        if next_url:
            request.session['fitbit_next'] = next_url
        else:
            request.session.pop('fitbit_next', None)

        callback_uri = request.build_absolute_uri(reverse('fitbit-complete'))
        fb = utils.create_fitbit(callback_uri=callback_uri)
        # returns back token_url and code ... set as _ for flake8
        token_url, _ = fb.client.authorize_token_url(redirect_uri=callback_uri)

        response = {'url': token_url}
        return Response(response)


class FitbitCompleteView(APIView):

    def post(self, request):
        try:
            code = request.data['code']
        except KeyError:
            return redirect('/500')

        callback_uri = request.build_absolute_uri(reverse('fitbit-complete'))
        fb = utils.create_fitbit(callback_uri=callback_uri)

        try:
            token = fb.client.fetch_access_token(code, callback_uri)
            access_token = token['access_token']
            fitbit_user_id = token['user_id']
        except KeyError:
            raise Http404('Invalid Token')

        user = request.user
        UserFitbit.objects.update_or_create(user=user, defaults={
            'fitbit_user_id': fitbit_user_id,
            'access_token': access_token,
            'refresh_token': token['refresh_token'],
            'expires_at': token['expires_at'],
        })

        next_url = request.session.pop('fitbit_next', None) or utils.get_setting(
            'FITBIT_LOGIN_REDIRECT')

        response = {'next_url': next_url}
        return Response(response)


class FitbitUserAuthCheck(APIView):
    # Simple class to check if a user has authorized Fitbit Credentials
    # Used by the frontend to decide which modal to display
    permission_classes = (IsAuthenticated, )
    url = 'fitbit-user-auth-check'

    def get(self, request):
        data = is_integrated(request.user)
        return Response(data)


class FitbitUserUpdateSleepHistory(APIView):
    # This concept isn't really RESTful (and more akin to SOA),
    # but I can't tell if it's really worth it either to make it a resource
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'fitbit-api-sync'
    url = 'fitbit-user-update-sleep-history'

    def post(self, request):
        data = request.data
        user = request.user

        try:
            initial_data = {
                'start_date': data['start_date'],
                'end_date': data['end_date'],
            }
        except (MultiValueDictKeyError, KeyError) as exc:
            return Response('Missing POST parameters {}'.format(exc), status=400)

        serializer = FitbitAPIRequestSerializer(data=initial_data)
        serializer.is_valid(raise_exception=True)

        # send the job off to celery so it's an async task
        import_user_fitbit_history_via_api.delay(user=user, **serializer.validated_data)

        return Response(status=202)
