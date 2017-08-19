from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apis.fitbit import utils
from apis.fitbit.models import UserFitbit
from apis.fitbit.utils import is_integrated


class FitbitLoginView(TemplateView):

    @method_decorator(login_required)
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

        return redirect(token_url)


class FitbitCompleteView(APIView):

    @method_decorator(login_required)
    def get(self, request):
        try:
            code = request.GET['code']
        except KeyError:
            return redirect('/500')

        callback_uri = request.build_absolute_uri(reverse('fitbit-complete'))
        fb = utils.create_fitbit(callback_uri=callback_uri)

        try:
            token = fb.client.fetch_access_token(code, callback_uri)
            access_token = token['access_token']
            fitbit_user = token['user_id']
        except KeyError:
            raise Http404('Invalid Token')

        user = request.user
        UserFitbit.objects.update_or_create(user=user, defaults={
            'fitbit_user': fitbit_user,
            'access_token': access_token,
            'refresh_token': token['refresh_token'],
            'expires_at': token['expires_at'],
        })

        next_url = request.session.pop('fitbit_next', None) or utils.get_setting(
            'FITBIT_LOGIN_REDIRECT')

        return redirect(next_url)


class FitbitUserAuthCheck(APIView):
    # Simple class to check if a user has authorized Fitbit Credentials
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        data = is_integrated(request.user)
        return Response(data)
