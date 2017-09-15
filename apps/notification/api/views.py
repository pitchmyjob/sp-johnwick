from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from apps.notification.models import Notification


class NotificationApiView(APIView):

    def get(self, request):
        response = Notification().run(id=self.request.user.id, page=request.query_params.get('page', None))
        serializer = NotificationSerializer(data=response)
        serializer.is_valid()

        Notification().update(id=self.request.user.id)

        return Response(serializer.data, status=status.HTTP_200_OK)
