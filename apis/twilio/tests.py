from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from apis.twilio.views import verify_phone_number
from betterself.users.models import UserPhoneNumber

User = get_user_model()


class TestTwilioVerifies(TestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')

    def test_twilio_verifies(self):
        valid_phone_number = '+16175231234'
        instance = UserPhoneNumber.objects.create(user=self.test_user, phone_number=valid_phone_number)
        verify_phone_number(valid_phone_number)

        instance.refresh_from_db()
        self.assertTrue(instance.is_verified)

    def test_twilio_wont_verify(self):
        valid_phone_number = '+16175231234'
        UserPhoneNumber.objects.create(user=self.test_user, phone_number=valid_phone_number)

        with self.assertRaises(ObjectDoesNotExist):
            verify_phone_number('1234')
