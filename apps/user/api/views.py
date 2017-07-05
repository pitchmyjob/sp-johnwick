from rest_framework import generics, viewsets, mixins, decorators
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from apps.authentication.api.mixins import AuthMeMixin
from apps.authentication.models import User
from apps.spitch.models import Spitch
from apps.ask.models import Ask

from .paginations import SpitchPagination
from apps.worker.tasks import sync_user


class UserMeRetrieveApi(AuthMeMixin, generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer

    def perform_update(self, serializer):
        super(UserMeRetrieveApi, self).perform_update(serializer)
        sync_user.delay(self.request.user.id, "update")



class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.detail_route(methods=['get'])
    def datas(self, request, pk):
        return Response(UserDatasSerializer(instance=self.get_object()).data)



class SpitchUserList(generics.ListAPIView):
    serializer_class = SpitchSerializer
    pagination_class = SpitchPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Spitch.objects.filter(user=pk)


class AskUserList(generics.ListAPIView):
    serializer_class = UserAskSerializer
    pagination_class = SpitchPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Ask.objects.filter(user=pk)



# class UserTopSpitcher(generics.ListAPIView):
#     serializer_class = UserTopSpitcher
#
#     def get_queryset(self):
#         return User.objects.order_by('-id')[:10]
