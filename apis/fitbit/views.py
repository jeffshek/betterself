from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from apis.fitbit import utils
from apis.fitbit.models import UserFitbit


class FitbitLoginView(APIView):
    def get(self, request):
        next_url = request.GET.get('next', None)
        if next_url:
            request.session['fitbit_next'] = next_url
        else:
            request.session.pop('fitbit_next', None)

        callback_uri = request.build_absolute_uri(reverse('fitbit-complete'))
        fb = utils.create_fitbit(callback_uri=callback_uri)
        token_url, code = fb.client.authorize_token_url(redirect_uri=callback_uri)

        return redirect(token_url)


class FitbitCompleteView(APIView):
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
            return redirect(reverse('fitbit-error'))

        # if UserFitbit.objects.filter(fitbit_user=fitbit_user).exists():
        #     return redirect(reverse('fitbit-error'))

        user = request.user
        fbuser, _ = UserFitbit.objects.update_or_create(user=user, defaults={
            'fitbit_user': fitbit_user,
            'access_token': access_token,
            'refresh_token': token['refresh_token'],
            'expires_at': token['expires_at'],
        })

        # Add the Fitbit user info to the session
        # fb = utils.create_fitbit(**fbuser.get_user_data())
        # request.session['fitbit_profile'] = fb.user_profile_get()

        next_url = request.session.pop('fitbit_next', None) or utils.get_setting(
            'FITAPP_LOGIN_REDIRECT')

        return redirect(next_url)
