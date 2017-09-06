from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from betterself import celery_app


@celery_app.task()
def create_demo_fixtures_for_user(user):
    fixtures_builder = DemoHistoricalDataBuilder(user)
    fixtures_builder.create_historical_fixtures()
