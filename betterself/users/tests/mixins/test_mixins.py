from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_CREDENTIALS = {
    'username': 'tester',
    'email': 'username@gmail.com',
    'password': 'secret_password',
}

SECONDARY_DEFAULT_CREDENTIALS = {
    'username': 'tester2',
    'email': 'username@gmail.com',  # i hate that django allows multiple emails to be created
    'password': 'secret_password',
}


class UsersTestsFixturesMixin(object):
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

    @classmethod
    def create_user_fixtures(cls):
        # setup the user once
        cls.user_1 = cls.create_user()
        # create some random fake user_2 to test duplicates
        cls.user_2 = cls.create_user(SECONDARY_DEFAULT_CREDENTIALS)
        cls.default_user, _ = User.objects.get_or_create(username='default')
