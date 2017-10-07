import datetime
import logging

from django.conf import settings
from twilio.rest import Client

from betterself import celery_app
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.models import SupplementReminder

logger = logging.getLogger(__name__)


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
def send_verification_text(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body="https://betterself.io - Please verify your number by replying with 'VERIFY'. Thanks!")


@celery_app.task
def send_thanks_for_verification_text(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body='https://betterself.io - Your phone number has been verified. Thanks!')


@celery_app.task
def send_log_confirmation(supplement_event, number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # if only you could send http links prettier in text messages
    message = "https://betterself.io/dashboard/log/supplements_events/ - We've logged your record of {}. Thanks!"\
        .format(supplement_event.supplement.name)
    client.messages.create(
        to=number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message)


@celery_app.task
def send_text_reminders(beat_time=None):
    if not beat_time:
        beat_time = datetime.datetime.now()

    start_time = get_start_time_interval_from_beat_time(beat_time)
    end_time = get_end_time_interval_from_beat_time(beat_time)

    queryset = SupplementReminder.objects.filter(user__userphonenumber__is_verified=True)
    # if the end_time is tomorrow, then we just want everything past 11:55
    if end_time.hour == 0:
        queryset = queryset.filter(reminder_time__gte=start_time)
    else:
        # if you don't do this, if someone puts a time that's before the current
        # hour/minute, it'll automatically send a first text, which seems silly
        queryset = queryset.filter(reminder_time__gte=start_time, reminder_time__lt=end_time)

    # if its already sent for today, don't include it to send
    date_today = get_current_utc_time_and_tz().date()

    queryset = queryset.objects.exclude(last_sent_reminder_time__date=date_today)

    for result in queryset:
        send_supplement_reminder.delay(result.id)


@celery_app.task
def send_supplement_reminder(supplement_reminder_id):
    reminder = SupplementReminder.objects.get(id=supplement_reminder_id)

    reminder_text = 'BetterSelf.io - Daily Reminder to take {} of {}! Reply DONE when done!'.format(
        reminder.quantity, reminder.supplement.name)

    phone_to_text = reminder.user.userphonenumber.phone_number.as_e164

    # autosave prior to sending to client, just in case twilio is down
    # this would queue up to many things
    reminder.last_sent_reminder_time = get_current_utc_time_and_tz()
    reminder.save()

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_to_text,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=reminder_text)
