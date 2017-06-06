from django.db import models

from betterself.base_models import BaseModelWithUserGeneratedContent


class Vendor(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = 'vendors'

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'user')
