from django.db import models

from betterself.mixins import BaseModel


class Vendors(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)  # RFC3696 compliant, probably means just get spammed harder


