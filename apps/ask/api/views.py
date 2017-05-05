from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import *


class AskCreateApiView(generics.CreateAPIView):
    serializer_class = AskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)