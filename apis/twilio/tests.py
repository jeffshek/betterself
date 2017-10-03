import datetime

import pytz
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from apis.twilio.tasks import get_start_time_interval_from_beat_time, \
    get_end_time_interval_from_beat_time
from apis.twilio.views import verify_phone_number, log_supplement_event
from betterself.users.models import UserPhoneNumber
from events.models import SupplementReminder, SupplementEvent
from supplements.models import Supplement

User = get_user_model()


class TestTwilioVerifies(TestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')

    def test_twilio_verifies(self):
        valid_phone_number = '+16175231234'
        instance = UserPhoneNumber.objects.create(user=self.test_user, phone_number=valid_phone_number)
        verify_phone_number(valid_phone_number)

        instance.refresh_from_db()
        self.assertTrue(instance.is_verified)

    def test_twilio_wont_verify(self):
        valid_phone_number = '+16175231234'
        UserPhoneNumber.objects.create(user=self.test_user, phone_number=valid_phone_number)

        with self.assertRaises(ObjectDoesNotExist):
            verify_phone_number('1234')


class TestTwilioLogsEvents(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_phone_number = '+16175231234'
        cls.test_user = User.objects.create_user('testuser', 'testpassword')

        # create a supplement
        supplement = Supplement.objects.create(user=cls.test_user, name='Twilio')
        UserPhoneNumber.objects.create(user=cls.test_user, phone_number=cls.valid_phone_number, is_verified=True)
        last_sent = datetime.datetime(2017, 1, 1, tzinfo=pytz.UTC)
        reminder_time = datetime.time(10, 11)
        SupplementReminder.objects.create(
            supplement=supplement, user=cls.test_user, last_sent_reminder_time=last_sent,
            reminder_time=reminder_time, quantity=1
        )

        super().setUpTestData()

    def test_supplement(self):
        self.assertEqual(SupplementEvent.objects.count(), 0)

        log_supplement_event(self.valid_phone_number)

        self.assertEqual(SupplementEvent.objects.count(), 1)


class TestTimeRounding(TestCase):
    def test_start_time_interval(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=6)
        response = get_start_time_interval_from_beat_time(random_datetime)

        # this should round down to the 5 minute mark
        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 5)

    def test_start_time_interval_at_0_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=0)
        response = get_start_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 0)

    def test_start_time_interval_at_59_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=59)
        response = get_start_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 55)

    def test_start_time_interval_at_1_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=1)
        response = get_start_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 0)

    def test_end_time_interval_at_1_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=1)
        response = get_end_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 5)

    def test_end_time_interval_at_5_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=5)
        response = get_end_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 13)
        self.assertEqual(response.minute, 10)

    def test_end_time_interval_at_59_min(self):
        random_datetime = datetime.datetime(2017, 1, 1, hour=13, minute=59)
        response = get_end_time_interval_from_beat_time(random_datetime)

        self.assertEqual(response.hour, 14)
        self.assertEqual(response.minute, 0)
