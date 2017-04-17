# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import AuthRegisterApiView, AuthRsRegisterApiView

urlpatterns = [
    url(r'^auth/token-auth/', obtain_jwt_token),
    url(r'^auth/register/$', AuthRegisterApiView.as_view(), name='register-user'),
    url(r'^auth/register/rs/$', AuthRsRegisterApiView.as_view(), name='register-user-rs'),
]