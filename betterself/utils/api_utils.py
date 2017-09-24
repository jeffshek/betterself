import datetime
import logging
import numpy as np

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
        'uniqueKey': key,
        'value': value,
        'data_type': data_type,
        'label': label
    }

    return response


def guess_data_type(value):
    if isinstance(value, str):
        return 'str'
    elif isinstance(value, int):
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
        raise Exception
