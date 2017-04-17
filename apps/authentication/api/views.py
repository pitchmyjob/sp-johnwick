# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserEmailRegisterSerialier, UserRsRegisterSerialier

from ..models import User

class AuthRegisterApiView(generics.CreateAPIView):
    serializer_class = UserEmailRegisterSerialier
    permission_classes = (AllowAny,)

class AuthRsRegisterApiView(generics.CreateAPIView):
    serializer_class = UserRsRegisterSerialier
    permission_classes = (AllowAny,)