# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import *

urlpatterns = [
    url(r'^auth/token-auth/$', obtain_jwt_token),
    url(r'^auth/facebook/$', AuthFacebookView.as_view()),

    url(r'^auth/register/$', AuthRegisterApiView.as_view(), name='register-user'),

    url(r'^auth/register/facebook/$', AuthFacebookRegisterApiView.as_view(), name='register-user-rs'),

    url(r'^auth/presigned-url/$', AuthGeneratePresignedUrl.as_view(), name='presignated-url'),
    url(r'^auth/check/$', AuthEmailUsernameCheckApiView.as_view(), name='checkrun'),
]