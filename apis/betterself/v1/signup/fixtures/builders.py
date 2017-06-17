import datetime

import numpy as np
import pandas as pd
import random

from apis.betterself.v1.signup.fixtures.factories import DemoSupplementEventFactory, DemoActivityEventFactory
from apis.betterself.v1.signup.fixtures.fixtures import SUPPLEMENTS_FIXTURES, USER_ACTIVITY_EVENTS
from events.models import SleepEventLog, DailyProductivityLog


class DemoHistoricalDataBuilder(object):
    """
    Builds a lot of fixtures together so the demo is comprehensible
    """

    def __init__(self, user):
        self.user = user
        self.hour_series = range(0, 24)

        historical_data_points_quantity = 90

        # use pandas to generate a nifty index of timestamps
        end_date = datetime.date.today()
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

    def create_historical_fixtures(self):
        for timestamp in self.date_series:
            for activity_name, activity_details in USER_ACTIVITY_EVENTS.items():
                self.build_events(activity_name, activity_details, timestamp, DemoActivityEventFactory)

            for supplement_name, supplement_details in SUPPLEMENTS_FIXTURES.items():
                self.build_events(supplement_name, supplement_details, timestamp, DemoSupplementEventFactory)

        # Include the baseline randomness of sleep along with how supplements impacted it
        total_sleep = self.sleep_series + self.sleep_impact_series

        sleep_logs = []
        for index, sleep_amount in total_sleep.iteritems():
            sleep_event = SleepEventLog(user=self.user, sleep_time_minutes=sleep_amount, source='web', date=index)
            sleep_logs.append(sleep_event)

        SleepEventLog.objects.bulk_create(sleep_logs)

        # let's do some real basic estimation that sleep is the most important thing to productivity
        # and then let's add how productivity
        baseline_productivity_series = total_sleep / 2
        productivity_series = self.productivity_impact_series + baseline_productivity_series

        # if the productivity falls below zero ... just make it a zero, since negative
        # productivity doesn't really make sense either.
        productivity_series[productivity_series < 0] = 0

        productivity_logs = []
        for index, productivity_amount in productivity_series.iteritems():
            log = DailyProductivityLog(user=self.user, date=index, very_productive_time_minutes=productivity_amount,
                                       very_distracting_time_minutes=productivity_amount / 2)
            productivity_logs.append(log)

        DailyProductivityLog.objects.bulk_create(productivity_logs)

    def build_events(self, activity_name, index_details, timestamp, factory_type):
        events_to_create = random.randint(*index_details['quantity_range'])
        # no replacement, grab a sample hour from each one, because timestamps have to be unique
        random_hours = random.sample(self.hour_series, events_to_create)
        for _ in range(events_to_create):
            random_hour = random_hours.pop()
            random_time = timestamp.to_datetime().replace(hour=random_hour)
            # use a factory boy instance to create the record
            factory_type(user=self.user, name=activity_name, time=random_time)

        productivity_impact_minutes = self.calculate_productivity_impact(events_to_create, index_details)
        self.productivity_impact_series[timestamp] += productivity_impact_minutes

        sleep_impact_minutes = self.calculate_sleep_impact(events_to_create, index_details)
        self.sleep_impact_series[timestamp] += sleep_impact_minutes
