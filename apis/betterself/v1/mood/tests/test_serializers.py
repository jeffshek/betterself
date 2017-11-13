import datetime

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase

from apis.betterself.v1.mood.serializers import MoodReadOnlySerializer, MoodCreateUpdateSerializer
from betterself.utils.date_utils import get_current_utc_time_and_tz
from events.fixtures.factories import UserMoodLogFactory
from events.models import UserMoodLog, WEB_INPUT_SOURCE

User = get_user_model()


class TestMoodSerializers(TestCase):
    FIXTURES_SIZE = 50

    @classmethod
    def setUpTestData(cls):
        cls.random_user = User.objects.create_user(username='hello')
        now = get_current_utc_time_and_tz()
        for subtract_seconds in range(0, cls.FIXTURES_SIZE):
            time = now - relativedelta(seconds=subtract_seconds)
            UserMoodLogFactory(time=time, user=cls.random_user)

    def test_fixture_generation(self):
        self.assertEqual(UserMoodLog.objects.all().count(), self.FIXTURES_SIZE)

    def test_mood_serializer_read(self):
        mood_log = UserMoodLog.objects.first()
        serializer = MoodReadOnlySerializer(mood_log)

        data = serializer.data
        self.assertEqual(data['value'], mood_log.value)
        self.assertEqual(data['uuid'], str(mood_log.uuid))
        # this is the default
        self.assertEqual(data['source'], WEB_INPUT_SOURCE)

        parsed_time = parser.parse(data['time'])
        self.assertEqual(parsed_time, mood_log.time)

        # we shouldn't be passing back user
        self.assertTrue('user' not in data)

    def test_create_mood_serializer(self):
        value = 5
        data = {'value': value}
        serializer = MoodCreateUpdateSerializer(data=data, context={'user': self.random_user})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        instance = serializer.save()
        self.assertEqual(instance.value, value)

    def test_update_mood_serializer(self):
        # get any instance that is less than 6. doesn't matter what it is, just need to update it
        update_instance = UserMoodLog.objects.filter(value__lte=6).first()

        data = {'value': 9}

        serializer = MoodCreateUpdateSerializer(instance=update_instance, data=data)
        self.assertTrue(serializer.is_valid())

        instance = serializer.save()
        self.assertEqual(instance.value, 9)

    def test_update_mood_serializer_time(self):
        update_instance = UserMoodLog.objects.first()

        update_time = datetime.datetime(2000, 1, 1, tzinfo=pytz.UTC)

        data = {
            'time': update_time,
            'value': 1
        }

        serializer = MoodCreateUpdateSerializer(instance=update_instance, data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        self.assertEqual(instance.time, update_time)
