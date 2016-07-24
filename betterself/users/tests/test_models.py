from test_plus.test import TestCase

from betterself.users.tests.mixins.test_mixins import UsersTestsMixin


class TestUser(TestCase, UsersTestsMixin):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )

    def test_user_login(self):
        credentials = {
            'username': 'test_user_1',
            'email': 'username@gmail.com',
            'password': 'secret_password',
        }

        self.create_user(credentials)
        result = self.client.login(**credentials)

        self.assertEqual(result, True)
