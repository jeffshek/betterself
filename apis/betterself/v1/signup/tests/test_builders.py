from django.contrib.auth import get_user_model
from django.test import TestCase

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from events.models import SupplementReminder
from supplements.models import Supplement

User = get_user_model()


class TestDemoFixturesBuilder(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test-demo-user')

    def test_builder(self):
        builder = DemoHistoricalDataBuilder(self.user)
        builder.create_historical_fixtures()

    def test_calculate_productivity_impact(self):
        details = {
            'quantity_range': (0, 5),
            'net_productivity_impact_per_quantity': 30,
            'peak_threshold_quantity': 3,
            'post_threshold_impact_on_productivity_per_quantity': -30,
            'sleep_impact_per_quantity': -10,
        }

        result = DemoHistoricalDataBuilder.calculate_productivity_impact(5, details)
        # if the quantity is 5 ... the result should be
        # 30 + 30 + 30 + (-30) (-30) = 30
        self.assertEqual(result, 30)

        # test the peak
        result = DemoHistoricalDataBuilder.calculate_productivity_impact(3, details)
        self.assertEqual(result, 90)

        # test sample size of 1
        result = DemoHistoricalDataBuilder.calculate_productivity_impact(1, details)
        self.assertEqual(result, 30)


class TestSupplementReminderBuilder(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        builder = DemoHistoricalDataBuilder(cls.default_user)
        builder.create_historical_fixtures()
        builder.create_supplement_reminders()

        super().setUpTestData()

    def test_supplement_reminders_creation(self):
        supplement_count = Supplement.objects.filter(user=self.default_user).count()
        supplement_reminder_count = SupplementReminder.objects.filter(user=self.default_user).count()
        self.assertEqual(supplement_count, supplement_reminder_count)
