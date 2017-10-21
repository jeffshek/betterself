import datetime
import itertools

from pytz import timezone

from events.fixtures.factories import SupplementEventFactory, DailyProductivityLogFactory, UserActivityFactory, \
    UserActivityEventFactory
from events.models import INPUT_SOURCES
from supplements.fixtures.factories import SupplementFactory
from supplements.models import UserSupplementStack

VALID_QUANTITIES = range(1, 30)
STATIC_DATE = datetime.datetime(2016, 12, 31)
eastern_tz = timezone('US/Eastern')
STATIC_DATE = eastern_tz.localize(STATIC_DATE)
GENERATED_DATES = [STATIC_DATE + datetime.timedelta(days=x) for x in range(0, 30)]


def generate_test_cases_for_events():
    """
    Generate an array of all the test cases by multiplying all the possibilities by themselves
    """
    test_cases = itertools.product(VALID_QUANTITIES, INPUT_SOURCES)
    return test_cases


def generate_unique_index_per_supplements_and_time(supplements_used):
    unique_index = itertools.product(supplements_used, GENERATED_DATES)
    return unique_index


class SupplementEventsFixturesGenerator(object):
    @staticmethod
    def create_fixtures(user):
        supplement_1 = SupplementFactory(user=user, name='Fish Oil')
        supplement_2 = SupplementFactory(user=user, name='Snake Oil')
        supplement_3 = SupplementFactory(user=user, name='Truffle Oil')

        supplements_used = [supplement_1, supplement_2, supplement_3]

        # test unique_index where database constrains to only one
        unique_index = generate_unique_index_per_supplements_and_time(supplements_used)

        # test random non-unique identifiers like quantity of 50 and different input sources
        test_cases = generate_test_cases_for_events()

        for supplement, event_time in unique_index:
            # use generator and get the next result
            # we can't do for loop because this is a unique constraint on table
            # here, we are just getting the next possible q/input ONCE versus
            # in each of the for loops
            #
            # TODO - Refactor your stupidity
            quantity, input_source = test_cases.__next__()

            SupplementEventFactory(quantity=quantity, source=input_source,
                                   time=event_time, user=user, supplement=supplement)


class UserSupplementStackFixturesGenerator(object):
    @staticmethod
    def create_fixtures(user):
        supplement_1 = SupplementFactory(user=user, name='Fish Oil')
        supplement_2 = SupplementFactory(user=user, name='Snake Oil')
        supplement_3 = SupplementFactory(user=user, name='Truffle Oil')

        first_stack = UserSupplementStack.objects.create(user=user, name='first_stack')
        first_stack.supplements.add(*[supplement_1, supplement_2])

        second_stack = UserSupplementStack.objects.create(user=user, name='second_stack')
        second_stack.supplements.add(*[supplement_1, supplement_2, supplement_3])


class ProductivityLogFixturesGenerator(object):
    @staticmethod
    def create_fixtures(user, days_fwd_amt=35):
        start_date = datetime.date(2016, 12, 15)
        for days_fwd in range(days_fwd_amt):
            fixture_date = start_date + datetime.timedelta(days=days_fwd)
            DailyProductivityLogFactory(user=user, date=fixture_date)

    @staticmethod
    def create_fixtures_starting_from_today(user, periods_back):
        end_date = datetime.date.today()

        for days_back in range(periods_back):
            fixture_date = end_date - datetime.timedelta(days=days_back)
            DailyProductivityLogFactory(user=user, date=fixture_date)


class UserActivityEventFixturesGenerator(object):
    @staticmethod
    def create_fixtures(user):
        activity_names = [
            'Ran',
            'Bike',
            'Swim',
            'Eat',
            'Sleep',
            'Fight Crime'
        ]

        for activity in activity_names:
            user_activity = UserActivityFactory(user=user, name=activity)
            UserActivityEventFactory(user_activity=user_activity, user=user)
