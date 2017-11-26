from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from betterself.users.models import TIMEZONE_CHOICES

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

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'timezone', 'supplements', 'phone_number', 'email')

    def create(self, validated_data):
        # Override create in this serializer so we can use the function create_user
        # thus resulting in salted password hashes
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, validated_data):
        cleaned_supplements = self._clean_supplements(validated_data['supplements'])
        validated_data['supplements'] = cleaned_supplements
        return validated_data

    def get_phone_number(self, user):
        try:
            user_phone_number = user.userphonenumberdetails
        except ObjectDoesNotExist:
            return
        else:
            phone_number = user_phone_number.phone_number
            phone_number_serialized = phone_number.as_e164
            return phone_number_serialized

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
