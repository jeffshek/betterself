from events.models import SupplementLog
from supplements.models import IngredientComposition, Supplement, Ingredient, Measurement
from vendors.models import Vendor

VALID_REST_RESOURCES = [
    SupplementLog,
    Supplement,
    IngredientComposition,
    Ingredient,
    Measurement,
    Vendor
]

# a lot of frontend (react) depends on a uniqueKey to render rows, in this case, do something here that makes rendering
# all the rows a little bit easier. in most circumstances, for any resources that are directly related to a model
# uuid is fine, but not all resources are django models, so uniqueKey comes in handy
UNIQUE_KEY_CONSTANT = 'uniqueKey'

DAILY_FREQUENCY = 'daily'
MONTHLY_FREQUENCY = 'monthly'
