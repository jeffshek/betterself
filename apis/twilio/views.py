from django.http.response import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from betterself.users.models import UserPhoneNumber


def verify_phone_number(number):
    # technically, this could sometimes error out if a user deletes his/her account
    # and then decides to reply verify ... but that seems unlikely, instead if there is an error
    # let's see what it is
    phone_number = UserPhoneNumber.objects.get(phone_number=number)
    phone_number.is_verified = True
    phone_number.save()

    return Response(status=202)


class TwilioTextMessageResponse(APIView):
    permission_classes = []

    def post(self, request):
        account_cid = request.data['AccountSid']
        if settings.TWILIO_ACCOUNT_SID != account_cid:
            raise HttpResponseForbidden

        phone_number = request.data['From']
        message = request.data['Body'].upper().strip()

        if 'VERIFY' in message:
            return verify_phone_number(phone_number)

        return Response()
