import datetime
from django.utils import timezone

from rest_framework import status, generics
from django.db.models import Count

from ..models import Ask
from .serializers import *


class AskCreateApiView(generics.CreateAPIView):
    serializer_class = AskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TrendTagsListApiView(generics.ListAPIView):
    serializer_class = TrendTagSerializer

    def get_queryset(self):
        d =  timezone.now() - datetime.timedelta(days=30)
        return Tag.objects.filter(asktag__created__gte = d).annotate(ct=Count("tag")).order_by('-ct')[:10]



class SearchAskListApiView(generics.ListAPIView):
    serializer_class = AskListSerializer

    def get_queryset(self):
        return Ask.objects.filter(user__followers__user = self.request.user).distinct().order_by("-created")[:10]