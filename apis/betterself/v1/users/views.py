from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from apis.betterself.v1.signup.serializers import CreateUserSerializer
from apis.betterself.v1.users.serializers import PhoneNumberSerializer
from apis.twilio.tasks import send_verification_text
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

        request_number = serializer.data['phone_number']
        existing_number = UserPhoneNumber.objects.filter(phone_number=request_number).exclude(user=user)
        if existing_number.exists():
            if existing_number.filter(is_verified=True).exists():
                return Response('{} Phone number exists to someone else!'.format(request_number), status=400)
            else:
                # if another person hasn't verified it, then it was probably entered by accident
                existing_number.delete()

        user_phone_number, _ = UserPhoneNumber.objects.update_or_create(user=user, defaults=serializer.data)
        # if the number hasn't been verified, but the user is adding another supplement-reminder
        if not user_phone_number.is_verified:
            send_verification_text.delay(user_phone_number.phone_number)

        return Response(PhoneNumberSerializer(user_phone_number).data)
