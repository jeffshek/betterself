from django.test import TestCase

from apis.betterself.v1.constants import UNIQUE_KEY_CONSTANT
from betterself.utils.api_utils import get_api_value_formatted


class TestAPIResponse(TestCase):
    def test_get_api_value_formatted_as_expected(self):
        key = 'one-potato'
        value = 5
        data_type = 'number'
        label = 'Potato Quantity'

        data = get_api_value_formatted(
            key=key,
            value=value,
            data_type=data_type,
            label=label
        )

        expected_response = {
            UNIQUE_KEY_CONSTANT: key,
            'value': 5,
            'data_type': 'number',
            'label': 'Potato Quantity'
        }

        self.assertEqual(
            data, expected_response
        )
