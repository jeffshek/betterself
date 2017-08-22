from django.contrib.auth import get_user_model
from django.db import models


# Taken from django-fitbit, many thanks to them! Package is good, just wanted CBVs
# https://github.com/orcasgit/django-fitbit/blob/master/fitapp/models.py

USER_MODEL = get_user_model()


class UserFitbit(models.Model):
    """ A user's fitbit credentials, allowing API access """
    user = models.OneToOneField(USER_MODEL)
    fitbit_user_id = models.CharField(max_length=32, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    # this is a floatfield since it's returned that way by fitbit
    expires_at = models.FloatField()

    def __str__(self):
        return self.user.__str__()

    def refresh_cb(self, token):
        """ Called when the OAuth token has been refreshed """
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        self.expires_at = token['expires_at']
        self.save()

    def get_user_data(self):
        return {
            'user_id': self.fitbit_user_id,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'refresh_cb': self.refresh_cb,
        }
