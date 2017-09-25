import datetime

import pytz
from dateutil import relativedelta

UTC_TZ = pytz.timezone('UTC')


def days_ago_from_current_day(days):
    now = datetime.datetime.utcnow()
    # make sure the timezone is added to the datetime, otherwise many warnings
    now = UTC_TZ.localize(now)
    date_days_ago = now - relativedelta.relativedelta(days=days)
    return date_days_ago


def get_current_date_months_ago(months):
    today = datetime.date.today()
    return today - relativedelta.relativedelta(months=months)


def get_current_date_years_ago(years):
    today = datetime.date.today()
    return today - relativedelta.relativedelta(years=years)


def get_current_date_days_ago(days_ago):
    today = datetime.date.today()
    return today - relativedelta.relativedelta(days=days_ago)


def get_midnight_datetime_from_date_parameter(user, date):
    # for a date, transform it into a datetime object at midnight
    time_serialized = datetime.datetime.combine(date, datetime.datetime.min.time())
    return user.pytz_timezone.localize(time_serialized)
