from django.contrib.auth import get_user_model
from django.test import TestCase

from apis.betterself.v1.signup.serializers import UserDetailsSerializer
from betterself.users.models import UserPhoneNumberDetails

User = get_user_model()


class TestUserSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.default_user, _ = User.objects.get_or_create(username='default')
        super().setUpTestData()

    def test_user_details_serializer(self):
        a_cool_user_name = 'a_cool_user_name'
        cool_user, _ = User.objects.get_or_create(username=a_cool_user_name)
        serializer = UserDetailsSerializer(cool_user)

        data = serializer.data

        self.assertEqual(data['username'], a_cool_user_name)
        self.assertEqual(data['phone_number'], None)
        self.assertEqual(data['uuid'], str(cool_user.uuid))

    def test_user_details_serializer_with_phone_number(self):
        good_number = '+16171234567'
        UserPhoneNumberDetails.objects.create(user=self.default_user, phone_number=good_number)
        serializer = UserDetailsSerializer(self.default_user)

        data = serializer.data

        self.assertEqual(data['phone_number'], good_number)
