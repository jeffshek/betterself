from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.views import UserProductivityAnalytics
from betterself.users.tests.mixins.test_mixins import UsersTestsFixturesMixin


class TestUserProductivityViews(TestCase, UsersTestsFixturesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.create_user_fixtures()
        cls.url = reverse(UserProductivityAnalytics.namespace_url_name)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user_1)
        super().setUp()

    def test_analytics_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_analytics_no_login_and_redirected(self):
        new_client = APIClient()
        response = new_client.get(self.url)
        self.assertEqual(response.status_code, 302)
