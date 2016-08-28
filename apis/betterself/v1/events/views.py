from apis.betterself.v1.events.serializers import SupplementEventSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1
from events.models import SupplementEvent


class SupplementEventView(BaseGenericListCreateAPIViewV1):
    serializer_class = SupplementEventSerializer
    model = SupplementEvent
