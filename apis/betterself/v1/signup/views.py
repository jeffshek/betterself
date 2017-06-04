from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer
from betterself.users.models import DemoUserLog


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
        # have username be demo-username
        # so demo-usernames are then easy to tell

        # TODO
        # generate a fake username
        # generate a fake password
        serializer = CreateUserSerializer(data=request.data)
        # if serializer isn't valid, just quit early
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        # save the instance
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        json_response = serializer.data
        json_response['token'] = token.key

        # create a log to show this is a demo user
        DemoUserLog.objects.create(user=user)

        # now create a bunch of fake data for the account
        return Response(json_response, status=HTTP_201_CREATED)
