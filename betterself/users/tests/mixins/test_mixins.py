from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_CREDENTIALS = {
    'username': 'default',
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
    def create_authenticated_user_on_client(cls, client, user):
        client.force_login(user)

        # just a quick check just in case
        assert user.is_authenticated()

        return client

    @classmethod
    def create_user_fixtures(cls):
        # setup the user once
        cls.user_1, _ = User.objects.get_or_create(username='default')

        # create some random fake user_2 to test duplicates and no information leakage
        cls.user_2 = cls.create_user(SECONDARY_DEFAULT_CREDENTIALS)
