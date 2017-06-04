from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """
    The create and update serializers "could" be combined, but I rather
    be explicit separation for now, I can combine them later -- just don't want to build
    tests that assume they're nested.
    """
    username = serializers.CharField(max_length=32,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )

    password = serializers.CharField(min_length=8, max_length=32, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        # override create step to use native django create_user
        # so that the password will be salted/hashed

        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        return user
