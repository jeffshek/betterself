from django.test import TestCase
from rest_framework import serializers

from apis.betterself.v1.events.serializers import valid_daily_max_minutes, SupplementEventReadOnlySerializer
from events.fixtures.factories import SupplementEventFactory
from supplements.fixtures.factories import SupplementFactory


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


class TestSupplementEventSerializer(TestCase):
    def test_supplement_serializer(self):
        supplement = SupplementFactory(notes='gibberish')
        event = SupplementEventFactory(supplement=supplement)
        serializer = SupplementEventReadOnlySerializer(event)

        dict_responses = serializer.data

        self.assertEqual(dict_responses['uuid'], str(event.uuid))
        self.assertEqual(dict_responses['notes'], event.notes)
        self.assertEqual(dict_responses['quantity'], event.quantity)
