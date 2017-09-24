from events.models import SupplementEvent
from supplements.models import IngredientComposition, Supplement, Ingredient, Measurement
from vendors.models import Vendor

VALID_REST_RESOURCES = [
    SupplementEvent,
    Supplement,
    IngredientComposition,
    Ingredient,
    Measurement,
    Vendor
]

UNIQUE_KEY_CONSTANT = 'uniqueKey'
