import datetime
import itertools

from pytz import timezone

from events.fixtures.factories import SupplementEventFactory
from events.models import INPUT_SOURCES
from supplements.fixtures.factories import SupplementFactory

VALID_QUANTITIES = range(1, 30)
STATIC_DATE = datetime.datetime(2016, 12, 31)
eastern_tz = timezone('US/Eastern')
STATIC_DATE = eastern_tz.localize(STATIC_DATE)
GENERATED_DATES = [STATIC_DATE - datetime.timedelta(days=x) for x in range(0, 10)]


def generate_test_cases_for_events():
    """
    Generate an array of all the test cases by multiplying all the possibilities by themselves
    """
    test_cases = itertools.product(VALID_QUANTITIES, INPUT_SOURCES)
    return test_cases


def generate_unique_index_per_supplements_and_time(supplements_used):
    unique_index = itertools.product(supplements_used, GENERATED_DATES)
    return unique_index


class EventModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls, user):
        supplement_1 = SupplementFactory(user=user)
        supplement_2 = SupplementFactory(user=user, name='Snake Oil')
        supplement_3 = SupplementFactory(user=user, name='Truffle Oil')

        supplements_used = [supplement_1, supplement_2, supplement_3]

        # test unique_index where database constrains to only one
        unique_index = generate_unique_index_per_supplements_and_time(supplements_used)

        # test random non-unique identifiers like quantity of 50 and different input sources
        test_cases = generate_test_cases_for_events()

        for supplement, event_time in unique_index:
            # use generator and get the next result (we can't do for loop because this is a unique constraint on table)
            quantity, input_source = test_cases.__next__()

            SupplementEventFactory(quantity=quantity, source=input_source,
                time=event_time, user=user, supplement=supplement)
