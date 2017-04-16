# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import UserRegisterSerialier

from ..models import User

class AuthRegisterApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerialier
    permission_classes = (AllowAny,)