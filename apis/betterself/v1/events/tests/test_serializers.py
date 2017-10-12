from django.test import TestCase
from rest_framework import serializers

from apis.betterself.v1.events.serializers import valid_daily_max_minutes


class TestSerializerUtils(TestCase):
    @staticmethod
    def test_regular_max_minutes():
        valid_daily_max_minutes(600)

    def test_more_than_daily_max_minutes(self):
        with self.assertRaises(serializers.ValidationError):
            valid_daily_max_minutes(3601)

    def test_less_than_zero_max_minutes(self):
        with self.assertRaises(serializers.ValidationError):
            valid_daily_max_minutes(-50)
