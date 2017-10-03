import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.views import APIView

from betterself.users.models import UserPhoneNumber
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.models import SupplementReminder, SupplementEvent, TEXT_MSG_SOURCE

logger = logging.getLogger(__name__)


def verify_phone_number(number):
    # technically, this could sometimes error out if a user deletes his/her account
    # and then decides to reply verify ... but that seems unlikely, instead if there is an error
    # let's see what it is
    phone_number = UserPhoneNumber.objects.get(phone_number=number)
    phone_number.is_verified = True
    phone_number.save()

    return Response(status=202)


def log_supplement_event(number):
    try:
        # no spoofing
        user = UserPhoneNumber.objects.get(phone_number=number, is_verified=True).user
    except ObjectDoesNotExist:
        logger.exception('Could Not Find {}'.format(number))
        return Response(status=404)

    supplement_reminder = SupplementReminder.objects.filter(user=user).order_by('last_sent_reminder_time').last()

    SupplementEvent.objects.create(
        supplement=supplement_reminder.supplement,
        source=TEXT_MSG_SOURCE,
        quantity=supplement_reminder.quantity,
        time=get_current_utc_time_and_tz(),
        user=user
    )

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

        if 'DONE' in message:
            return log_supplement_event(phone_number)

        return Response()
