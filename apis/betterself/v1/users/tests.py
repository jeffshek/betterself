from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apis.betterself.v1.signup.fixtures.builders import DemoHistoricalDataBuilder

User = get_user_model()


class UserExportAllDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api-user-export-all-data')
        cls.user = User.objects.create(username='demo')

        builder = DemoHistoricalDataBuilder(cls.user)
        builder.create_historical_fixtures()

        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_export_view(self):
        # TODO - switch to loading the response in an excel reader
        # and measuring the columns are equal to what one would expect
        response = self.client.get(self.url)
        response_content_disposition = response.get('Content-Disposition')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('attachment; filename=' in response_content_disposition)
        self.assertTrue('xlsx' in response_content_disposition)

    def test_export_view_with_user_and_no_data(self):
        user = User.objects.create(username='demo-with-no-data')
        client = APIClient()
        client.force_authenticate(user)

        response = client.get(self.url)
        print (response.status_code)

    def test_export_view_not_logged_in(self):
        client = APIClient()
        response = client.get(self.url)
        # not authorized
        self.assertEqual(response.status_code, 403)
