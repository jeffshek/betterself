# -*- coding: utf-8 -*-
import uuid as uuid

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    # most of the models have id equivalent to uuid, but for User (since this
    # is so inherent in Django) i've left as uuid ... this can be refactored
    # later to replace the id column after i feel comfortable with it. right now
    # it's just not worth the risk of finding out having a uuid as the primary key
    # on user breaks things i don't know about
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    # since this is dealing with a lot of different timezones - enforce a user input
    timezone = models.CharField(max_length=50, choices=[(x, x) for x in pytz.common_timezones], default='US/Eastern')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @staticmethod
    def get_default_user():
        default_user, _ = User.objects.get_or_create(username='default')
        return default_user

    @staticmethod
    def get_default_user_id():
        return User.get_default_user().id
