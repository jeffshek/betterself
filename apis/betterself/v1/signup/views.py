from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer
from apis.betterself.v1.signup.tasks import create_demo_fixtures_for_user
from betterself.users.models import DemoUserLog
from config.settings.constants import TESTING, LOCAL
from events.utils.default_events_builder import DefaultEventsBuilder
from supplements.models import Supplement

User = get_user_model()


class CreateUserView(APIView):
    # Limit the amount of signups from any individual ip to 5 a day
    # to prevent spam issues
    throttle_scope = 'signups'
    # If the user is just signing up, one would assume they can't have authentication yet ...
    permission_classes = ()

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Per some signups, custom supplements are pre-filled for custom users
        supplements = serializer.validated_data.pop('supplements')

        user = serializer.save()

        # if there's a custom set of supplements that were added along with signup
        # this signup is coming programmatically and supplements should automatically be created
        if supplements:
            for supplement_name in supplements:
                Supplement.objects.get_or_create(user=user, name=supplement_name)
        else:
            # build default events for new-users
            builder = DefaultEventsBuilder(user)
            builder.build_defaults()

        token, _ = Token.objects.get_or_create(user=user)
        json_response = serializer.data
        json_response['token'] = token.key

        return Response(json_response, status=HTTP_201_CREATED)


class CreateDemoUserView(APIView):
    """
    Used to create a demo user with preloaded fixtures to illustrate features
    """
    throttle_scope = 'demo_signups'
    # If the user is just signing up, one would assume they can't have authentication yet ...
    permission_classes = ()

    def get(self, request):
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

        # during testing and local environments, we want immediately the fixtures to be created
        # otherwise for actual use cases, have it be done async
        if settings.DJANGO_ENVIRONMENT in (TESTING, LOCAL):
            create_demo_fixtures_for_user(user)
        else:
            create_demo_fixtures_for_user.delay(user)

        return Response(json_response, status=HTTP_201_CREATED)
