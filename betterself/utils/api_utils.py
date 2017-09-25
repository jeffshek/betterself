import datetime
import logging
import numpy as np

from apis.betterself.v1.constants import UNIQUE_KEY_CONSTANT

logger = logging.getLogger(__name__)


def get_api_value_formatted(key, value, label, data_type=None):
    """
    Force a constraint to make sure going forward all the API responses are ideal

    Key: Should be unique for a complete response (think of React's key concept)
    Value : Value of Object
    data_type : string, value, etc.
    label : What the value represents (in proper English)
    """
    if not data_type:
        data_type = guess_data_type(value)

    # taking a step back and thinking about this, the whole dict within key structure is stupid
    response = {
        UNIQUE_KEY_CONSTANT: key,
        'value': value,
        'data_type': data_type,
        'label': label
    }

    return response


def guess_data_type(value):
    """
    Passes logic to the frontend, a string that becomes useful in rendering how a specific value should be displayed
    ie. if certain datetime constants are passed, that can be used to generate links
    """
    if isinstance(value, str):
        return 'str'
    elif isinstance(value, (int, np.int64, np.int32)):
        return 'int'
    elif isinstance(value, (float, np.float64)):
        return 'float'
    elif isinstance(value, list):
        return 'list'
    elif isinstance(value, datetime.date):
        return 'date'
    elif isinstance(value, datetime.datetime):
        return 'datetime'
    else:
        logger.exception('Unable to determine data type of {}'.format(value))
