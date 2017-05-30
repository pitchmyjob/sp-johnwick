import boto3

from rest_framework import decorators, permissions, status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404

from ..models import Spitch
from apps.ask.models import Ask
from .serializers import *


class NewSpitch(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, pk, format=None):
        ask = get_object_or_404(Ask, pk=pk)
        file = request.data['file']
        file.content_type = "video/mp4"
        spitch = Spitch.objects.create(user=self.request.user, ask=ask)
        spitch.spitch = file
        spitch.save()
        return Response(status=status.HTTP_201_CREATED)


class SpitchViewSet(viewsets.ModelViewSet):
    serializer_class = SpitchSerializer

    def get_queryset(self):
        return Spitch.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = InitializeSpitchSerializer

        if self.request.method == 'PUT' or self.request.method == "PATH":
            serializer_class = EndSpitchSerializer

        return serializer_class

    def perform_update(self, serializer):
        super(SpitchViewSet, self).perform_update(serializer)
        self.execute_sfn(self.get_object())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.detail_route(methods=['put', 'patch'], parser_classes = (FileUploadParser,) )
    def clip(self, request, pk):
        spitch = self.get_object()
        file = request.data['file']
        key = settings.MEDIAFILES_LOCATION+"/"+str(self.request.user.id)+"/spitch/"+str(spitch.id)+"/"+str(file.name)
        s3 = boto3.resource('s3')
        # s3.Bucket('spitchdev-bucket-uwfmzpv98dvk').put_object(Key=key, Body=file, ContentType='video/mp4')
        upload = Spitch.objects.select_for_update().filter(id=spitch.id).update(clip_uploaded=F('clip_uploaded') + 1)
        spitch = Spitch.objects.get(id=spitch.id)
        self.execute_sfn(spitch)
        return Response(status=status.HTTP_201_CREATED)

    def execute_sfn(self, spitch):
        if spitch.clip_total > 0:
            if spitch.clip_total == spitch.clip_uploaded:
                print('OKKKK')