import datetime

import numpy as np
import pandas as pd
import random
from django.utils import timezone

from apis.betterself.v1.signup.fixtures.factories import SupplementReminderFactory
from apis.betterself.v1.signup.fixtures.fixtures import SUPPLEMENTS_FIXTURES, USER_ACTIVITY_EVENTS
from betterself.utils.date_utils import UTC_TZ
from events.models import DailyProductivityLog, SleepActivity, UserActivityLog, SupplementEvent, UserActivity
from supplements.models import Supplement


class DemoHistoricalDataBuilder(object):
    """
    Builds a lot of fixtures together so the demo is comprehensible
    """

    def __init__(self, user, periods_back=30):
        self.user = user
        self.hour_series = range(0, 24)

        historical_data_points_quantity = periods_back

        end_date = timezone.now()

        # use pandas to generate a nifty index of timestamps, use timezone to remove warning signals
        self.date_series = pd.date_range(end=end_date, freq='D', periods=historical_data_points_quantity)

        # build a series that shows the impact of what supplements/events have on sleep
        self.sleep_impact_series = pd.Series(0, index=self.date_series)
        self.productivity_impact_series = pd.Series(0, index=self.date_series)

        self.sleep_series = self._get_random_sleep_series(self.date_series)

        # Create a cache here because creating many events is very slow on Production ...
        # so create a cache of commonly used Django objects and then create a bunch of events that
        # need this foreign key, so we can use bulk_create
        self.user_activities = {}
        self.supplements = {}

    @staticmethod
    def calculate_productivity_impact(quantity, event_details):
        # Pseudo science to show some results
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

    def create_user_activities(self):
        for activity_name in USER_ACTIVITY_EVENTS.keys():
            user_activity = UserActivity.objects.create(name=activity_name, user=self.user)
            self.user_activities[activity_name] = user_activity

    def create_supplements(self):
        for supplement_name in SUPPLEMENTS_FIXTURES.keys():
            supplement = Supplement.objects.create(name=supplement_name, user=self.user)
            self.supplements[supplement_name] = supplement

    def create_historical_fixtures(self):
        user_activities_bulk_create = []
        supplement_logs_bulk_create = []

        self.create_user_activities()
        self.create_supplements()

        for timestamp in self.date_series:
            for activity_name, activity_details in USER_ACTIVITY_EVENTS.items():
                activity = self.user_activities[activity_name]

                events = self.build_events(activity, activity_details, timestamp, UserActivityLog)
                user_activities_bulk_create.extend(events)

            for supplement_name, supplement_details in SUPPLEMENTS_FIXTURES.items():
                supplement = self.supplements[supplement_name]

                supplement_events = self.build_events(supplement, supplement_details, timestamp, SupplementEvent)
                supplement_logs_bulk_create.extend(supplement_events)

        UserActivityLog.objects.bulk_create(user_activities_bulk_create)
        SupplementEvent.objects.bulk_create(supplement_logs_bulk_create)

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

    def build_events(self, parent_event_key, event_details, timestamp, event_type):
        events = []

        events_to_create = random.randint(*event_details['quantity_range'])
        # use random.sample for no replacement, because timestamps have to be unique
        random_hours = random.sample(self.hour_series, events_to_create)

        for _ in range(events_to_create):
            random_hour = random_hours.pop()
            random_time = timestamp.to_pydatetime().replace(hour=random_hour)

            if event_type == UserActivityLog:
                event = event_type(user=self.user, user_activity=parent_event_key, time=random_time)
            elif event_type == SupplementEvent:
                event = event_type(user=self.user, supplement=parent_event_key, time=random_time, quantity=1)
            else:
                raise Exception

            events.append(event)

        productivity_impact_minutes = self.calculate_productivity_impact(events_to_create, event_details)
        self.productivity_impact_series[timestamp] += productivity_impact_minutes

        sleep_impact_minutes = self.calculate_sleep_impact(events_to_create, event_details)
        self.sleep_impact_series[timestamp] += sleep_impact_minutes

        return events

    def create_supplement_reminders(self, limit=None):
        supplements = self.supplements.values()
        for count, supplement in enumerate(supplements):
            if limit and count == limit:
                return

            SupplementReminderFactory(supplement=supplement, user=self.user)
