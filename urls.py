# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include([
        url(r'^', include('apps.authentication.urls')),
        url(r'^', include('apps.relation.urls')),
        url(r'^', include('apps.ask.urls')),
        url(r'^', include('apps.user.urls')),
        url(r'^', include('apps.notification.urls')),
        url(r'^', include('apps.spitch.urls')),
    ])),
    url(r'^admin/', admin.site.urls),
]
