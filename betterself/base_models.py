# maybe change the location of this file, but don't have a better place at the moment
import uuid as uuid

from django.conf import settings
from django.db import models


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
