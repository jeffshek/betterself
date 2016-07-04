# -*- coding: utf-8 -*-
import pytz

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    # since this is dealing with a lot of different timestamps
    # enforce a user input
    timezone = models.CharField(max_length=50, choices=[(x, x) for x in pytz.common_timezones], default='US/Eastern')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
