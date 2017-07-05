from rest_framework import generics

from apps.feed.models import Feed
from apps.core.api.mixins import ContextMixin
from .serializers import FeedListSerializer
from . pagination import FeedListPagination


class FeedListApiView(ContextMixin, generics.ListAPIView):
    serializer_class = FeedListSerializer
    pagination_class = FeedListPagination

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)
