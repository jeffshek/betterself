import uuid as uuid

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField

from betterself.base_models import BaseModel

TIMEZONE_CHOICES = [(x, x) for x in pytz.common_timezones]


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    # since this is dealing with a lot of different timezones - enforce a user input
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='US/Eastern')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def pytz_timezone(self):
        return pytz.timezone(self.timezone)


class DemoUserLog(BaseModel):
    """
    Create a log of all demo users that are generated. That way all demo users
    can be periodically purged, but still offer a good experience for people
    interested in trying out features
    """
    user = models.OneToOneField(User, unique=True)

    class Meta:
        verbose_name = 'Demo User Log'
        verbose_name_plural = 'Demo User Logs'

    def __str__(self):
        return self.user.username


class UserPhoneNumberDetails(BaseModel):
    user = models.OneToOneField(User, unique=True)
    phone_number = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Phone Number'
        verbose_name_plural = 'User Phone Numbers'

    def __str__(self):
        return '{}-{}'.format(self.user, self.phone_number)


# Create a signal to be able to delete all demo-users easily so this
# can be cleaned up via admin
@receiver(post_delete, sender=DemoUserLog)
def post_delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
