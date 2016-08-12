from apis.betterself.v1.events.serializers import SupplementEventSerializer
from apis.betterself.v1.utils.views import BaseGenericListCreateAPIViewV1
from events.models import SupplementEvent


class SupplementEventView(BaseGenericListCreateAPIViewV1):
    serializer_class = SupplementEventSerializer
    model = SupplementEvent

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            queryset = self.model.objects.filter(name__iexact=name)
        else:
            queryset = self.model.objects.all()

        return queryset
