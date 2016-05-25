from django.db import models

from betterself.mixins import BaseModelWithUserGeneratedContent


class Vendor(BaseModelWithUserGeneratedContent):
    name = models.CharField(max_length=200)
    # EmailField is RFC3696 compliant, probably means just get spammed harder
    email = models.EmailField(max_length=254, null=True, blank=True)
    url = models.URLField(null=True, blank=True)


