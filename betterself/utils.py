import pytz
import datetime

from dateutil import relativedelta

UTC_TZ = pytz.timezone('UTC')


def create_django_choice_tuple_from_list(list_a):
    if list_a is None:
        return ()

    tuples_list = []
    for item in list_a:
        if isinstance(item, str):
            tuple_item_title = item.title()
        else:
            tuple_item_title = item

        tuple_item = (item, tuple_item_title)
        tuples_list.append(tuple_item)

    return tuple(tuples_list)


def days_ago_from_current_day(days):
    now = datetime.datetime.utcnow()
    # make sure the timezone is added to the datetime, otherwise many warnings
    now = UTC_TZ.localize(now)
    date_days_ago = now - relativedelta.relativedelta(days=days)
    return date_days_ago
