from rest_framework import generics, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from apps.authentication.api.mixins import AuthMeMixin
from apps.authentication.models import User


class UserMeRetrieveApi(AuthMeMixin, generics.RetrieveAPIView):
    serializer_class = UserMeSerializer


class UserRetrieveApi(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

