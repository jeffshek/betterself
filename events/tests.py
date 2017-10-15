import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from betterself.utils.date_utils import UTC_TZ
from events.models import SleepLog

User = get_user_model()


class SleepActivityModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_user = User.objects.create_user(username='Scottie')
        # pretend someone is sleeping from 1AM to 7AM
        start_time = datetime.datetime(2016, 1, 1, hour=1, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 1, 1, hour=7, tzinfo=UTC_TZ)

        # create an event that will be the basis of seeing if save validation works
        SleepLog.objects.create(user=cls.default_user, start_time=start_time, end_time=end_time)

    def test_sleep_activity_wont_let_overlaps_save(self):
        start_time = datetime.datetime(2016, 1, 1, hour=1, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 1, 1, hour=7, tzinfo=UTC_TZ)

        with self.assertRaises(ValidationError):
            SleepLog.objects.create(user=self.default_user, start_time=start_time, end_time=end_time)

    def test_sleep_activity_wont_let_start_time_overlaps_save(self):
        start_time = datetime.datetime(2016, 1, 1, hour=2, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 1, 1, hour=10, tzinfo=UTC_TZ)

        with self.assertRaises(ValidationError):
            SleepLog.objects.create(user=self.default_user, start_time=start_time, end_time=end_time)

    def test_sleep_activity_wont_let_end_time_overlaps_save(self):
        start_time = datetime.datetime(2016, 1, 1, hour=0, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 1, 1, hour=2, tzinfo=UTC_TZ)

        with self.assertRaises(ValidationError):
            SleepLog.objects.create(user=self.default_user, start_time=start_time, end_time=end_time)

    def test_sleep_activity_can_normally_save(self):
        start_time = datetime.datetime(2016, 2, 1, hour=0, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 2, 1, hour=2, tzinfo=UTC_TZ)

        result = SleepLog.objects.create(user=self.default_user, start_time=start_time, end_time=end_time)

        self.assertEqual(result.start_time, start_time)
        self.assertEqual(result.user, self.default_user)

    def test_sleep_activity_prevents_end_time_lt_start(self):
        start_time = datetime.datetime(2016, 2, 3, hour=0, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 2, 1, hour=2, tzinfo=UTC_TZ)

        with self.assertRaises(ValidationError):
            SleepLog.objects.create(user=self.default_user, start_time=start_time, end_time=end_time)

    def test_sleep_activity_allows_same_object_to_be_saved(self):
        start_time = datetime.datetime(2016, 1, 1, hour=1, tzinfo=UTC_TZ)
        end_time = datetime.datetime(2016, 1, 1, hour=7, tzinfo=UTC_TZ)

        sleep_log = SleepLog.objects.get(user=self.default_user, start_time=start_time, end_time=end_time)
        sleep_log.save()
