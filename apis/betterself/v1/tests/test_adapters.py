from apis.betterself.v1.adapters.dataframe import BetterSelfAPIAdapter
from apis.betterself.v1.tests.test_base import BaseAPIv1Tests
from betterself.users.models import User
from django.conf import settings


# python manage.py test apis.betterself.v1.tests.test_adapters
class TestAdapters(BaseAPIv1Tests):

    def setUp(self):
        super().setUp()

    def test_resources_get_on_adapter(self):
        default_user, _ = User.objects.get_or_create(username='default')
        adapter = BetterSelfAPIAdapter(default_user)
