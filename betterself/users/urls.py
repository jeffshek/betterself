# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from betterself.users import views

urlpatterns = [
    url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
]
