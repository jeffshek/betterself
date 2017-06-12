from rest_framework.response import Response
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer


class UserInfoView(APIView):
    def get(self, request):
        user = self.request.user
        return Response(CreateUserSerializer(user).data)
