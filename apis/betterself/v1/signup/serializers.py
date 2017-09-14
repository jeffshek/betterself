from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from betterself.users.models import TIMEZONE_CHOICES

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=32,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )

    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    timezone = serializers.ChoiceField(choices=TIMEZONE_CHOICES, default='US/Eastern')
    supplements = serializers.CharField(max_length=350, default=None)

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'timezone', 'supplements')

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
    def _clean_supplements(supplement_string):
        if not supplement_string:
            return

        supplements_cleaned = []
        supplements = supplement_string.split(',')
        for supplement in supplements:
            name = supplement.strip().title()
            supplements_cleaned.append(name)

        return supplements_cleaned
