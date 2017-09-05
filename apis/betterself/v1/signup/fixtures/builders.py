import datetime

import numpy as np
import pandas as pd
import random
from django.utils import timezone

from apis.betterself.v1.signup.fixtures.factories import DemoSupplementEventFactory, DemoActivityEventFactory
from apis.betterself.v1.signup.fixtures.fixtures import SUPPLEMENTS_FIXTURES, USER_ACTIVITY_EVENTS
from betterself.utils.date_utils import UTC_TZ
from events.models import DailyProductivityLog, SleepActivity, UserActivityEvent, SupplementEvent


class DemoHistoricalDataBuilder(object):
    """
    Builds a lot of fixtures together so the demo is comprehensible
    """

    def __init__(self, user):
        self.user = user
        self.hour_series = range(0, 24)

        historical_data_points_quantity = 30

        # use pandas to generate a nifty index of timestamps, use timezone to remove warning signals
        # switch a day back since utc time starts forward by everyone's calendars so much
        end_date = timezone.now() - datetime.timedelta(days=1)
        self.date_series = pd.date_range(end=end_date, freq='D', periods=historical_data_points_quantity)

        # build a series that shows the impact of what supplements/events have on sleep
        self.sleep_impact_series = pd.Series(0, index=self.date_series)
        self.productivity_impact_series = pd.Series(0, index=self.date_series)

        self.sleep_series = self._get_random_sleep_series(self.date_series)

    @staticmethod
    def calculate_productivity_impact(quantity, event_details):
        peak_threshold_quantity = event_details['peak_threshold_quantity']
        post_threshold_impact_on_productivity_per_quantity = event_details[
            'post_threshold_impact_on_productivity_per_quantity']
        net_productivity_impact_per_quantity = event_details['net_productivity_impact_per_quantity']

        if not peak_threshold_quantity:
            return net_productivity_impact_per_quantity * quantity

        if quantity > peak_threshold_quantity:
            negative_quantity = quantity - peak_threshold_quantity
            negative_quantity_minutes = post_threshold_impact_on_productivity_per_quantity * negative_quantity

            positive_quantity_minutes = peak_threshold_quantity * net_productivity_impact_per_quantity

            net_productivity_minutes = negative_quantity_minutes + positive_quantity_minutes
        else:
            net_productivity_minutes = quantity * net_productivity_impact_per_quantity

        return net_productivity_minutes

    @staticmethod
    def calculate_sleep_impact(quantity, event_details):
        return quantity * event_details['sleep_impact_per_quantity']

    @staticmethod
    def _get_random_sleep_series(index, mean=60 * 7, std_dev=60):
        """
        Generate a normal distribution of sleep patterns based around 7 hours of
        sleep a day
        """
        data_points_to_create = len(index)
        sleep_times = np.random.normal(loc=mean, scale=std_dev, size=data_points_to_create)
        sleep_series = pd.Series(sleep_times, index=index)
        return sleep_series

    def create_sleep_fixtures(self):
        # Include the baseline randomness of sleep along with how supplements impacted it
        self.total_sleep = self.sleep_series + self.sleep_impact_series

        sleep_logs = []
        for index, sleep_amount in self.total_sleep.iteritems():
            index_date = index.date()
            # always pretend a user is sleeping at 10 PM
            index_start_time = datetime.time(hour=22)

            index_start_datetime = datetime.datetime.combine(index_date, index_start_time)
            index_start_datetime = UTC_TZ.localize(index_start_datetime)

            index_end_datetime = index_start_datetime + datetime.timedelta(minutes=sleep_amount)

            sleep_event = SleepActivity(
                user=self.user, source='web',
                start_time=index_start_datetime,
                end_time=index_end_datetime
            )
            sleep_logs.append(sleep_event)

        SleepActivity.objects.bulk_create(sleep_logs)

    def create_historical_fixtures(self):
        user_activities_bulk_create = []
        supplement_logs_bulk_create = []

        for timestamp in self.date_series:
            for activity_name, activity_details in USER_ACTIVITY_EVENTS.items():
                # import ipdb; ipdb.set_trace()
                events = self.build_events(activity_name, activity_details, timestamp,
                                           DemoActivityEventFactory)
                user_activities_bulk_create.extend(events)

            for supplement_name, supplement_details in SUPPLEMENTS_FIXTURES.items():
                supplement_events = self.build_events(supplement_name, supplement_details, timestamp,
                                                      DemoSupplementEventFactory)
                supplement_logs_bulk_create.extend(supplement_events)

        UserActivityEvent.objects.bulk_create(user_activities_bulk_create)
        SupplementEvent.objects.bulk_create(supplement_logs_bulk_create)

        # import ipdb; ipdb.set_trace()

        # calculate how much sleep from a random normal distribution
        # and how supplements would impact it
        self.create_sleep_fixtures()

        # let's do some real basic estimation that sleep is the most important thing to productivity
        # and then let's add how productivity
        baseline_productivity_series = self.total_sleep / 2
        productivity_series = self.productivity_impact_series + baseline_productivity_series

        # if the productivity falls below zero ... just make it a zero, since negative
        # productivity doesn't really make sense either.
        productivity_series[productivity_series < 0] = 0

        productivity_logs = []
        for index, productivity_minutes in productivity_series.iteritems():
            half_productivity_minutes = productivity_minutes / 2
            neutral_time_minutes = random.randint(10, 30)
            distracting_time_minutes = random.randint(10, 30)

            log = DailyProductivityLog(user=self.user, date=index,
                                       very_productive_time_minutes=productivity_minutes,
                                       productive_time_minutes=half_productivity_minutes,
                                       neutral_time_minutes=neutral_time_minutes,
                                       distracting_time_minutes=distracting_time_minutes,
                                       very_distracting_time_minutes=productivity_minutes / 2)
            productivity_logs.append(log)

        DailyProductivityLog.objects.bulk_create(productivity_logs)

    def build_events(self, activity_name, index_details, timestamp, factory_type):
        events = []

        events_to_create = random.randint(*index_details['quantity_range'])
        # no replacement, grab a sample hour from each one, because timestamps have to be unique
        random_hours = random.sample(self.hour_series, events_to_create)
        for _ in range(events_to_create):
            random_hour = random_hours.pop()
            random_time = timestamp.to_pydatetime().replace(hour=random_hour)
            # use a factory boy instance to create the record
            event = factory_type.build(user=self.user, name=activity_name, time=random_time)
            events.append(event)

        productivity_impact_minutes = self.calculate_productivity_impact(events_to_create, index_details)
        self.productivity_impact_series[timestamp] += productivity_impact_minutes

        sleep_impact_minutes = self.calculate_sleep_impact(events_to_create, index_details)
        self.sleep_impact_series[timestamp] += sleep_impact_minutes

        return events
