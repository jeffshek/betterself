from django.conf import settings
from django.db import models


# CharField is at 500 because StackOverflow user reports an api key of 350 characters


class FitBitAPICredentials(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500)


class RescueTimeAPICredentials(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500)


class BetterSelfCredentials(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500)
