import pytz
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=32,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    timezone = serializers.ChoiceField(pytz.common_timezones, default='US/Eastern')

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'timezone')

    def create(self, validated_data):
        # Override create in this serializer so we can use the function create_user
        # thus resulting in salted password hashes
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password, **validated_data)
        return user
