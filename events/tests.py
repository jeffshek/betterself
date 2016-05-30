from django.test import TestCase


class EventsModelsTests(TestCase):
    def test_all_models_in_test_have_required_users(self):
        # made this mistake where user wasn't required when first making event models ... realized
        # what good is an event if it isn't tied to a user?
        pass
