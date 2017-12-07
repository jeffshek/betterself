from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from betterself.users.models import UserPhoneNumberDetails, TIMEZONE_CHOICES

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. "
            'Up to 15 digits allowed.')

User = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    timezone = serializers.ChoiceField(choices=TIMEZONE_CHOICES, default='US/Eastern')
    supplements = serializers.CharField(max_length=350, default=None)
    phone_number = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(required=False)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'timezone', 'supplements', 'phone_number', 'email', 'token')

    def create(self, validated_data):
        # Override create in this serializer so we can use the function create_user
        # thus resulting in salted password hashes
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, validated_data):
        cleaned_supplements = self._clean_supplements(validated_data['supplements'])
        validated_data['supplements'] = cleaned_supplements
        return validated_data

    @staticmethod
    def get_phone_number(user):
        try:
            user_phone_number = user.userphonenumberdetails
        except ObjectDoesNotExist:
            return
        else:
            phone_number = user_phone_number.phone_number
            phone_number_serialized = phone_number.as_e164
            return phone_number_serialized

    @staticmethod
    def get_token(instance):
        """ Gets the API Token if it exists """
        try:
            return instance.auth_token.key
        except ObjectDoesNotExist:
            token, _ = Token.objects.get_or_create(user=instance)
            return token.key

    @staticmethod
    def _clean_supplements(supplement_string):
        if not supplement_string:
            return

        supplements_cleaned = []
        supplements = supplement_string.split(',')
        for supplement in supplements:
            # urls coming from the web with have %20, but it really means a space
            name = supplement.strip().title().replace('%20', ' ')
            supplements_cleaned.append(name)

        return supplements_cleaned


class PhoneNumberDetailsSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex])
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ['phone_number', 'is_verified']
        model = UserPhoneNumberDetails
