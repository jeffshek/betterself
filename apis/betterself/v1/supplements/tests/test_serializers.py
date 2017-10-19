# Didn't think testing serializers via unit tests until I had done a lot of integration tests with views
from django.contrib.auth import get_user_model
from django.test import TestCase

from apis.betterself.v1.supplements.serializers import UserSupplementStackCreateSerializer
from events.fixtures.mixins import UserSupplementStackFixturesGenerator
from supplements.models import UserSupplementStack

User = get_user_model()


class TestSupplementStackSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(username='potato')
        UserSupplementStackFixturesGenerator.create_fixtures(cls.user_1)
        super().setUpTestData()

    def test_serializer(self):
        UserSupplementStack.objects.all()

        all_supplement_stacks = UserSupplementStack.objects.all()

        for stack in all_supplement_stacks:
            serialized_data = UserSupplementStackCreateSerializer(instance=stack).data
            self.assertEqual(stack.supplements.count(), len(serialized_data['supplements']))
