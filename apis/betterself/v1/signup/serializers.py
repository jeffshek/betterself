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

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'timezone')

    def create(self, validated_data):
        # Override create in this serializer so we can use the function create_user
        # thus resulting in salted password hashes
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        timezone = validated_data.pop('timezone')

        user = User.objects.create_user(username=username, password=password, timezone=timezone)
        return user
