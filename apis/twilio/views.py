import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.twilio.tasks import send_log_confirmation, send_thanks_for_verification_text
from betterself.users.models import UserPhoneNumberDetails
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.models import SupplementReminder, SupplementLog, TEXT_MSG_SOURCE

logger = logging.getLogger(__name__)


def verify_phone_number(number):
    # technically, this could sometimes error out if a user deletes his/her account
    # and then decides to reply verify ... but that seems unlikely, instead if there is an error
    # let's see what it is
    user_phone_number = UserPhoneNumberDetails.objects.get(phone_number=number)
    user_phone_number.is_verified = True
    user_phone_number.save()

    send_thanks_for_verification_text.delay(user_phone_number.phone_number.as_e164)

    return Response(status=202)


def log_supplement_event(number):
    try:
        # no spoofing
        user = UserPhoneNumberDetails.objects.get(phone_number=number, is_verified=True).user
    except ObjectDoesNotExist:
        logger.exception('Could Not Find {}'.format(number))
        return Response(status=404)

    supplement_reminder = SupplementReminder.objects.filter(user=user).order_by('last_sent_reminder_time').last()

    supplement_log = SupplementLog.objects.create(
        supplement=supplement_reminder.supplement,
        source=TEXT_MSG_SOURCE,
        quantity=supplement_reminder.quantity,
        time=get_current_utc_time_and_tz(),
        user=user
    )

    send_log_confirmation.delay(supplement_log, number)

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
