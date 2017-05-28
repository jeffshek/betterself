# maybe change the location of this file, but don't have a better place at the moment
import uuid as uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name if hasattr(self, 'name') else self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class BaseModelWithUserGeneratedContent(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    # restrict access to objects that only belong to a user or belong to "defaults"
    @classmethod
    def get_user_viewable_objects(cls, user):
        # TODO - remove this stupidity
        default_user = get_user_model().objects.get(username='default')
        queryset = cls.objects.filter(Q(user=user) | Q(user=default_user))
        return queryset
