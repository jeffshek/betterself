# Didn't think testing serializers via unit tests until I had done a lot of integration tests with views
from django.contrib.auth import get_user_model
from django.test import TestCase

from apis.betterself.v1.supplements.serializers import UserSupplementStackReadSerializer, \
    UserSupplementStackCreateUpdateSerializer
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
        all_supplement_stacks = UserSupplementStack.objects.all()

        for stack in all_supplement_stacks:
            serialized_data = UserSupplementStackReadSerializer(instance=stack).data
            self.assertEqual(stack.compositions.count(), len(serialized_data['compositions']))

    def test_updating_serializing(self):
        stack = UserSupplementStack.objects.first()
        stack_id = stack.id
        initial_data = UserSupplementStackCreateUpdateSerializer(instance=stack).data
        stack_compositions = initial_data['compositions']
        compositions_count = stack.compositions.count()

        self.assertTrue(compositions_count > 1)

        one_composition = stack_compositions[0:1]

        data = {}
        data['name'] = stack.name
        data['compositions'] = one_composition

        context = {}
        context['user'] = stack.user

        serializer = UserSupplementStackCreateUpdateSerializer(instance=stack, data=data, context=context)
        serializer.is_valid()
        serializer.save()

        revised_stack = UserSupplementStack.objects.get(id=stack_id)
        revised_composition_count = revised_stack.compositions.count()
        self.assertEqual(revised_composition_count, 1)
