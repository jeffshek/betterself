from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer


# copy and pasted, but with one caveat, the POST returns additional
# information that is used for additional logic (ie. timezone and set username logic)
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'username': user.username,
                'timezone': user.timezone,
            }
        )


class UserInfoView(APIView):
    def get(self, request):
        user = self.request.user
        return Response(CreateUserSerializer(user).data)
