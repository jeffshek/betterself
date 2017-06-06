import datetime

import pandas
import random
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apis.betterself.v1.signup.fixtures.factories import DemoSupplementEventFactory, DemoActivityEvent
from apis.betterself.v1.signup.fixtures.fixtures import SUPPLEMENTS_FIXTURES, USER_ACTIVITY_EVENTS
from apis.betterself.v1.signup.serializers import CreateUserSerializer
from betterself.users.models import DemoUserLog

User = get_user_model()


class CreateUserView(APIView):
    # Limit the amount of signups from any individual ip to 5 a day
    # to prevent spam issues
    throttle_scope = 'signups'
    # If the user is just signing up, one would assume they can't have authentication yet ...
    permission_classes = ()

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, _ = Token.objects.get_or_create(user=user)
            json_response = serializer.data
            json_response['token'] = token.key

            return Response(json_response, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CreateDemoUserView(APIView):
    """
    Used to create a demo user with preloaded fixtures to illustrate features
    """
    throttle_scope = 'demo_signups'
    # If the user is just signing up, one would assume they can't have authentication yet ...
    permission_classes = ()

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

    def post(self, request):
        fake = Faker()
        name = fake.name()

        # have username be demo-username, so demos-users are easy to tell
        username = 'demo-{name}'.format(name=name)
        username = slugify(username)

        # since these are demo accounts, just set the username/pass the same
        user = User.objects.create_user(username=username, password=username)

        # create a log to show this is a demo user
        DemoUserLog.objects.create(user=user)

        serializer = CreateUserSerializer(user)
        json_response = serializer.data

        token, _ = Token.objects.get_or_create(user=user)
        json_response['token'] = token.key

        # use pandas to generate a nifty index of timestamps
        start_date = datetime.datetime(2017, 1, 1)
        date_series = pandas.date_range(start_date, freq='D', periods=90)

        # create a series to randomly select hours in a day
        hour_series = range(0, 24)

        productivity_impacted_time = {date: 0 for date in date_series}
        # sleep_impacted_time = {date: 0 for date in date_series}

        for timestamp in date_series:
            for activity_name, index_details in USER_ACTIVITY_EVENTS.items():
                events_to_create = random.randint(*index_details['quantity_range'])
                random_hours = random.sample(hour_series, events_to_create)

                for _ in range(events_to_create):
                    random_hour = random_hours.pop()
                    random_time = timestamp.to_datetime().replace(hour=random_hour)

                    DemoActivityEvent(user=user, name=activity_name, time=random_time)

                productivity_impact_minutes = self.calculate_productivity_impact(events_to_create, index_details)
                productivity_impacted_time[timestamp] += productivity_impact_minutes

            for supplement, supplement_details in SUPPLEMENTS_FIXTURES.items():
                # select a random amount of events to create
                events_to_create = random.randint(*supplement_details['quantity_range'])
                random_hours = random.sample(hour_series, events_to_create)

                for _ in range(events_to_create):
                    random_hour = random_hours.pop()
                    # since time has to be unique select some random times
                    random_time = timestamp.to_datetime().replace(hour=random_hour)

                    DemoSupplementEventFactory(user=user, name=supplement, time=random_time)

        import pprint
        pprint.pprint(productivity_impacted_time)
        # print (UserActivityEvent.objects.all().count())
        return Response(json_response, status=HTTP_201_CREATED)
