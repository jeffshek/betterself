from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer
from apis.betterself.v1.users.serializers import PhoneNumberSerializer
from betterself.users.models import UserPhoneNumber


class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        return Response(CreateUserSerializer(user).data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response('User {} was deleted'.format(user), status=HTTP_202_ACCEPTED)


class UserPhoneNumberView(APIView):
    def get(self, request):
        user = request.user

        try:
            phone_number_instance = user.userphonenumber
        except ObjectDoesNotExist:
            return Response({}, status=204)

        return Response(PhoneNumberSerializer(phone_number_instance).data)

    def post(self, request):
        user = request.user

        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number, _ = UserPhoneNumber.objects.update_or_create(user=user, defaults=serializer.data)

        return Response(PhoneNumberSerializer(phone_number).data)
