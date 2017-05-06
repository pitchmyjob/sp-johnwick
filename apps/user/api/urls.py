# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^user/me/$', UserMeRetrieveApi.as_view(), name='user-me'),
    url(r'^user/(?P<pk>\d+)/$', UserRetrieveApi.as_view(), name='user'),
]