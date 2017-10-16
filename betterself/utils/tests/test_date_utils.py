from django.contrib.auth import get_user_model
from django.test import TestCase

from betterself.utils.date_utils import get_datetime_in_eastern_timezone, EASTERN_TZ

User = get_user_model()


class TestDateUtils(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_eastern_function_returns_eastern(self):
        datetime = get_datetime_in_eastern_timezone(2017, 1, 1, 1, 1, 1)
        self.assertEqual(datetime.tzinfo, EASTERN_TZ)
