from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_CREDENTIALS = {
    'username': 'tester',
    'email': 'username@gmail.com',
    'password': 'secret_password',
}


class UsersTestsMixin(object):
    @classmethod
    def create_user(cls, **kwargs):
        # pass username, email and password
        user = User.objects.create_user(**kwargs)
        return user

    @classmethod
    def create_authenticated_user(cls, client, credentials=DEFAULT_CREDENTIALS):
        user = cls.create_user(**credentials)
        client.force_authenticate(user)
        return user
