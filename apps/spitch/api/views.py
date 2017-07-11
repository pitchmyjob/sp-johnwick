import random
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.spitch.models import Spitch, Like
from apps.ask.models import Ask
from apps.worker.tasks import new_spitch, like_spitch
from .serializers import *
from ..video import Video


class RetrieveSpitch(generics.RetrieveAPIView):
    queryset = Spitch.objects.all()
    serializer_class = SpitchSerializer


class LikeSpitch(APIView):

    def post(self, request, pk=None, format=None):
        if "spitch" in request.data:
            spitch = get_object_or_404(Spitch, pk=request.data['spitch'])
            if spitch.likes.filter(user=self.request.user).exists():
                spitch.likes.filter(user=self.request.user).delete()
            else:
                Like.objects.create(spitch=spitch, user=self.request.user)
                like_spitch.delay(self.request.user.id, spitch.id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NewSpitch(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, pk, format=None):
        ask = get_object_or_404(Ask, pk=pk)
        file = request.data['file']
        file.content_type = "video/mp4"
        spitch = Spitch.objects.create(user=self.request.user, ask=ask, color=1)
        video = Video(file, self.request.user.id, spitch.id, ask.text, spitch.color)
        spitch.spitch = file
        spitch.photo.name = video.thumb_key
        spitch.thumb.name = video.color_key
        spitch.active = True
        spitch.save()
        new_spitch.delay(spitch.id)
        return Response({"thumb":spitch.thumb.url}, status=status.HTTP_201_CREATED)







#Plus tard ----------------------------------------------
class NewSpitchV2(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, pk, format=None):
        ask = get_object_or_404(Ask, pk=pk)
        file = request.data['file']
        # file.content_type = "video/mp4"
        spitch = Spitch.objects.create(user=self.request.user, ask=ask, color=1)
        video = VideoThumb(file, self.request.user.id, spitch.id, ask.text, spitch.color)
        spitch.spitch = file
        spitch.video.name = video.video_key
        spitch.photo.name = video.thumb_key
        spitch.thumb.name = video.color_key
        spitch.active = True
        spitch.save()
        new_spitch.delay(spitch.id)
        return Response({"video":spitch.video.url, "thumb":spitch.thumb.url}, status=status.HTTP_201_CREATED)
