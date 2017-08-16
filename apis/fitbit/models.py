from django.contrib.auth import get_user_model
from django.db import models


# Taken from django-fitbit, many thanks to them! Package is good, just wanted CBVs
# https://github.com/orcasgit/django-fitbit/blob/master/fitapp/models.py

USER_MODEL = get_user_model()


class UserFitbit(models.Model):
    """ A user's fitbit credentials, allowing API access """
    user = models.OneToOneField(USER_MODEL)
    # feel like a better representation is if this was called id
    fitbit_user = models.CharField(max_length=32, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    # not sure why this a floatfield
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
            'user_id': self.fitbit_user,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'refresh_cb': self.refresh_cb,
        }


class FitbitTimeSeriesDataType(models.Model):
    """
    This model is intended to store information about Fitbit's time series
    resources, documentation for which can be found here:
    https://dev.fitbit.com/docs/food-logging/#food-or-water-time-series
    https://dev.fitbit.com/docs/activity/#activity-time-series
    https://dev.fitbit.com/docs/sleep/#sleep-time-series
    https://dev.fitbit.com/docs/body/#body-time-series
    """
    foods = 0
    activities = 1
    sleep = 2
    body = 3

    CATEGORY_CHOICES = (
        (foods, 'foods'),
        (activities, 'activities'),
        (sleep, 'sleep'),
        (body, 'body'),
    )
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    resource = models.CharField(max_length=128)

    class Meta:
        unique_together = ('category', 'resource',)
        ordering = ['category', 'resource']

    def __str__(self):
        return self.path()

    def path(self):
        return '/'.join([self.get_category_display(), self.resource])


class FitbitTimeSeriesData(models.Model):
    """
    The purpose of this model is to store Fitbit user data obtained from their
    time series API:
    https://dev.fitbit.com/docs/food-logging/#food-or-water-time-series
    https://dev.fitbit.com/docs/activity/#activity-time-series
    https://dev.fitbit.com/docs/sleep/#sleep-time-series
    https://dev.fitbit.com/docs/body/#body-time-series
    """
    user = models.ForeignKey(USER_MODEL)
    resource_type = models.ForeignKey(FitbitTimeSeriesDataType)
    date = models.DateField()
    value = models.CharField(null=True, default=None, max_length=32)

    class Meta:
        unique_together = ('user', 'resource_type', 'date')

    def string_date(self):
        return self.date.strftime('%Y-%m-%d')
