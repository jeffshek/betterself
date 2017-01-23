import datetime
import itertools

from pytz import timezone

from events.fixtures.factories import SupplementEventFactory
from events.models import INPUT_SOURCES
from supplements.fixtures.factories import SupplementFactory

VALID_QUANTITIES = range(1, 6)
# generate a list of 10 days back, use a static date since I don't random data in tests
STATIC_DATE = datetime.datetime(2016, 12, 31)
eastern_tz = timezone('US/Eastern')
STATIC_DATE = eastern_tz.localize(STATIC_DATE)
GENERATED_DATES = [STATIC_DATE - datetime.timedelta(days=x) for x in range(0, 10)]


def generate_test_cases_for_events(supplements_used):
    test_cases = itertools.product(VALID_QUANTITIES, INPUT_SOURCES, GENERATED_DATES, supplements_used)
    return test_cases


class EventModelsFixturesGenerator(object):
    @classmethod
    def create_fixtures(cls, user):
        supplement_1 = SupplementFactory(user=user)
        supplement_2 = SupplementFactory(user=user, name='Snake Oil')
        supplement_3 = SupplementFactory(user=user, name='Truffle Oil')

        supplements_used = [supplement_1, supplement_2, supplement_3]

        test_cases = generate_test_cases_for_events(supplements_used)
        for test_case in test_cases:
            quantity = test_case[0]
            input_source = test_case[1]
            event_time = test_case[2]
            supplement = test_case[3]

            # if the quantity is zero, it's kind of dumb to create fixtures
            # that holds a zero value
            SupplementEventFactory(quantity=quantity, source=input_source,
                time=event_time, user=user, supplement=supplement)
