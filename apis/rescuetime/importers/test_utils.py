from django.test import TestCase

from apis.rescuetime.importers.utils import calculate_rescue_time_pulse


class TestRescueTimeImportersUtils(TestCase):
    def test_rescuetime_of_zero(self):
        pulse = calculate_rescue_time_pulse(0, 0, 0, 0, 0)
        self.assertEqual(pulse, 0)
