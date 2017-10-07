from django.core.validators import RegexValidator
from rest_framework import serializers

from betterself.users.models import UserPhoneNumberDetails

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. "
                                     'Up to 15 digits allowed.')


class PhoneNumberDetailsSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex])
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ['phone_number', 'is_verified']
        model = UserPhoneNumberDetails
