# maybe change the location of this file, but don't have a better place at the moment
from django.db import models


# make sure that create and modify are always the same structure
class BaseTimeModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
