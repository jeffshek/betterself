from rest_framework.generics import ListCreateAPIView

from apis.betterself.v1.mood.serializers import MoodReadOnlySerializer, MoodCreateUpdateSerializer
from apis.betterself.v1.utils.views import ReadOrWriteSerializerChooser, UUIDDeleteMixin
from config.pagination import ModifiedPageNumberPagination
from events.models import UserMoodLog


class UserMoodViewSet(ListCreateAPIView, ReadOrWriteSerializerChooser, UUIDDeleteMixin):
    model = UserMoodLog
    pagination_class = ModifiedPageNumberPagination
    read_serializer_class = MoodReadOnlySerializer
    write_serializer_class = MoodCreateUpdateSerializer

    def get_serializer_class(self):
        return self._get_read_or_write_serializer_class()

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
