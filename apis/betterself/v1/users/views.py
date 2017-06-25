from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer


class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        return Response(CreateUserSerializer(user).data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response('User {} was deleted'.format(user), status=HTTP_202_ACCEPTED)
