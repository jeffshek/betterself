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

from apis.betterself.v1.signup.fixtures.factories import DemoSupplementEventFactory
from apis.betterself.v1.signup.fixtures.fixtures import SUPPLEMENTS_FIXTURES
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
    Used to create a demo
    """
    throttle_scope = 'demo_signups'
    # If the user is just signing up, one would assume they can't have authentication yet ...
    permission_classes = ()

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
        #
        start_date = datetime.datetime(2017, 1, 1)
        date_series = pandas.date_range(start_date, freq='D', periods=90)
        hour_series = range(0, 24)

        for timestamp in date_series:
            for supplement, supplement_details in SUPPLEMENTS_FIXTURES.items():
                events_to_create = random.randint(*supplement_details['quantity_range'])
                random_hours = random.sample(hour_series, events_to_create)
                for _ in range(events_to_create):
                    random_hour = random_hours.pop()
                    random_time = timestamp.to_datetime().replace(hour=random_hour)

                    DemoSupplementEventFactory(user=user, name=supplement, time=random_time)

        return Response(json_response, status=HTTP_201_CREATED)
