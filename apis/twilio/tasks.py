import logging

from django.conf import settings
from twilio.rest import Client

from betterself import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def send_verification_text(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body="https://betterself.io - Please verify your number by replying with 'VERIFY'. Thank you!")
