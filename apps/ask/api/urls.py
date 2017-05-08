# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ask/$', AskCreateApiView.as_view(), name='create-ask'),
    url(r'^ask/search/$', SearchAskListApiView.as_view(), name='search-ask'),

    url(r'^trend/tag$', TrendTagsListApiView.as_view(), name='trend-tag'),
]