import datetime
import logging

from django.conf import settings
from twilio.rest import Client

from betterself import celery_app
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.models import SupplementReminder

logger = logging.getLogger(__name__)


@celery_app.task
def send_verification_text(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body="https://betterself.io - Please verify your number by replying with 'VERIFY'. Thank you!")


# celery heartbeat ticks every 5 minutes, do a range to select
def get_start_time_interval_from_beat_time(beat_time):
    start_hour = beat_time.hour
    start_minute = (beat_time.minute // 5) * 5
    start_time = datetime.time(hour=start_hour, minute=start_minute)
    return start_time


def get_end_time_interval_from_beat_time(beat_time):
    end_datetime = beat_time + datetime.timedelta(minutes=5)
    end_hour = end_datetime.hour
    end_minute = (end_datetime.minute // 5) * 5
    end_time = datetime.time(hour=end_hour, minute=end_minute)
    return end_time


@celery_app.task
def send_text_reminders(beat_time=None):
    if not beat_time:
        beat_time = datetime.datetime.now()

    start_time = get_start_time_interval_from_beat_time(beat_time)
    end_time = get_end_time_interval_from_beat_time(beat_time)

    queryset = SupplementReminder.objects.filter(user__userphonenumber__is_verified=True)
    if end_time.hour == 0:
        queryset = queryset.filter(reminder_time__gte=start_time)
    else:
        queryset = queryset.filter(reminder_time__gte=start_time, reminder_time__lte=end_time)

    for result in queryset:
        send_supplement_reminder.delay(result.id)


@celery_app.task
def send_supplement_reminder(supplement_reminder_id):
    reminder = SupplementReminder.objects.get(id=supplement_reminder_id)

    reminder_text = 'BetterSelf.io - Hi! Daily Reminder to take {} of {}. Reply DONE when taken!'.format(
        reminder.supplement.name, reminder.quantity)

    phone_to_text = reminder.user.userphonenumber.phone_number.as_e164
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        to=phone_to_text,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=reminder_text)

    reminder.last_sent_reminder_time = get_current_utc_time_and_tz
    reminder.save()
