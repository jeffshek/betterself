# maybe change the location of this file, but don't have a better place at the moment
from django.db import models
from django.conf import settings


# Most Django models should be derived from this ... impose that many classes have similar
# create / modify attributes
class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelWithUserGeneratedContent(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        abstract = True
