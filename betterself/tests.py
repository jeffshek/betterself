from django.test import TestCase

from betterself.utils import create_django_choice_tuple_from_list


class DataUtilsTester(TestCase):
    def test_create_django_choice_tuple_from_list(self):
        list_a = ['jack', 'jill']
        returned_tuple = create_django_choice_tuple_from_list(list_a)

        expected_result = (('jack', 'Jack'), ('jill', 'Jill'))
        self.assertEqual(returned_tuple, expected_result)

    def test_create_django_choice_tuple_from_list_with_strings(self):
        list_a = [1, 'jill']
        returned_tuple = create_django_choice_tuple_from_list(list_a)

        expected_result = ((1, 1), ('jill', 'Jill'))
        self.assertEqual(returned_tuple, expected_result)
