from events.models import UserActivity
from supplements.models import Ingredient, Measurement, IngredientComposition, Supplement

DEFAULT_ACTIVITIES = [
    'Meditated',
    'Jogged',
    'Brushed Teeth',
    'Cold Shower',
    'Ate Breakfast',
    'Wrote in Journal',
    'Drank Alcohol',
    'Hungover',
    'Walked to Work',
    'Went to Gym'
]

SPECIAL_ACTIVITIES = [
    'Got Married',
    'Started New Job',
    'Read Life-Changing Book',
    'Bought A Car',
]


class DefaultEventsBuilder(object):
    def __init__(self, user):
        self.user = user

    def build_defaults(self):
        self.build_default_supplements()
        self.build_default_activities()

    def build_default_supplements(self):
        caffeine_ingredient, _ = Ingredient.objects.get_or_create(
            user=self.user, name='Caffeine')

        mg_measurement = Measurement.objects.get(short_name='mg')

        # Make 50 and 100mg IngredientCompositions
        caffeine_50mg_composition, _ = IngredientComposition.objects.get_or_create(
            user=self.user,
            measurement=mg_measurement,
            quantity=50,
            ingredient=caffeine_ingredient
        )

        caffeine_100mg_composition, _ = IngredientComposition.objects.get_or_create(
            user=self.user,
            measurement=mg_measurement,
            quantity=100,
            ingredient=caffeine_ingredient
        )

        caffeine_200mg_composition, _ = IngredientComposition.objects.get_or_create(
            user=self.user,
            measurement=mg_measurement,
            quantity=200,
            ingredient=caffeine_ingredient
        )

        # Now create Supplements like Coffee / Black Tea
        # that all have differing amounts of Caffeine
        coffee, _ = Supplement.objects.get_or_create(
            user=self.user,
            name='Coffee'
        )
        coffee.ingredient_compositions.add(caffeine_200mg_composition)

        black_tea, _ = Supplement.objects.get_or_create(
            user=self.user,
            name='Black Tea'
        )
        black_tea.ingredient_compositions.add(caffeine_100mg_composition)

    def build_default_activities(self):
        for activity_name in DEFAULT_ACTIVITIES:
            UserActivity.objects.get_or_create(user=self.user, name=activity_name)

        for activity_name in SPECIAL_ACTIVITIES:
            UserActivity.objects.get_or_create(user=self.user, name=activity_name, is_significant_activity=True)
