import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.test import TestCase
from random import randint

from betterself.utils.date_utils import get_current_date_months_ago
from betterself.utils.pandas_utils import force_start_end_data_to_dataframe

User = get_user_model()


class PandasUtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')

    def _get_mock_dataframe(self, user):
        two_months_ago = get_current_date_months_ago(2)
        one_month_ago = get_current_date_months_ago(1)
        default_index = pd.date_range(start=two_months_ago, end=one_month_ago, freq='D')

        random_values = [randint(0, 3) for _ in default_index]

        mock_dataframe = pd.DataFrame(index=default_index, data=random_values)
        mock_dataframe = mock_dataframe.tz_localize(user.pytz_timezone)
        return mock_dataframe

    def test_dataframe_creation(self):
        start_date = get_current_date_months_ago(3)
        end_date = datetime.date.today()

        dataframe = self._get_mock_dataframe(self.default_user)

        dataframe_date_appended = force_start_end_data_to_dataframe(user=self.default_user, dataframe=dataframe,
            start_date=start_date, end_date=end_date)

        # if it's appended new dates correctly, the index will be greater than before
        self.assertGreater(dataframe_date_appended.index.size, dataframe.index.size)
