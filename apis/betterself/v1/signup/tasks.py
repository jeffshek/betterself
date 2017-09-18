from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder
from betterself import celery_app
from betterself.users.models import DemoUserLog

User = get_user_model()


@celery_app.task()
def create_demo_fixtures():
    fake = Faker()
    name = fake.name()

    # have username be demo-username, so demos-users are easy to tell
    username = 'demo-{name}'.format(name=name)
    username = slugify(username)

    # since these are demo accounts, just set the username/pass the same
    user, _ = User.objects.get_or_create(username=username)

    # create a log of this person as a demo user, otherwise we would never be able to tell if someone is a demo or not!
    _, created = DemoUserLog.objects.get_or_create(user=user)
    if not created:
        return

    fixtures_builder = DemoHistoricalDataBuilder(user, periods_back=120)
    fixtures_builder.create_historical_fixtures()
