from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_CREDENTIALS = {
    'username': 'tester',
    'email': 'username@gmail.com',
    'password': 'secret_password',
}


class UsersTestsMixin(object):
    @classmethod
    def create_user(cls, credentials=DEFAULT_CREDENTIALS):
        # pass username, email and password
        user = User.objects.create_user(**credentials)
        return user

    @classmethod
    def create_authenticated_user_on_client(cls, client, user, credentials=DEFAULT_CREDENTIALS):
        client.force_authenticate(user)

        successfully_login = client.login(**credentials)

        # just a quick check just in case
        assert user.is_authenticated()
        assert successfully_login

        return client
