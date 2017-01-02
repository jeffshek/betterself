import datetime
import itertools

from pytz import timezone

from events.fixtures.factories import SupplementEventFactory
from events.models import INPUT_SOURCES
from supplements.fixtures.factories import SupplementFactory

VALID_QUANTITIES = range(0, 5)
# generate a list of 10 days back, use a static date since I don't random data in tests
STATIC_DATE = datetime.datetime(2016, 12, 31)
eastern_tz = timezone('US/Eastern')
STATIC_DATE = eastern_tz.localize(STATIC_DATE)
GENERATED_DATES = [STATIC_DATE - datetime.timedelta(days=x) for x in range(0, 10)]


def generate_test_cases_for_events():
    test_cases = itertools.product(VALID_QUANTITIES, INPUT_SOURCES, GENERATED_DATES)
    return test_cases


class EventModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls, user):
        supplement = SupplementFactory(user=user)
        test_cases = generate_test_cases_for_events()
        for test_case in test_cases:
            quantity = test_case[0]
            input_source = test_case[1]
            event_time = test_case[2]
            SupplementEventFactory(quantity=quantity, source=input_source,
                time=event_time, user=user, supplement=supplement)
