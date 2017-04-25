# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import boto3

from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import get_object_or_404

from .serializers import UserRsRegisterSerializer, UserEmailRegisterSerializer, FacebookTwitterLoginSerializer
from ..models import User
from apps.relation.models import FacebookFriend
from apps.authentication.facebook import Facebook



class AuthFacebookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        if "token" in request.data:
            fb = Facebook(request.data['token'])
            user = get_object_or_404(User, idsn=fb.get_id())

            if user.type == "facebook":
                return Response({"token": user.get_token()}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthRegisterApiView(generics.CreateAPIView):
    serializer_class = UserEmailRegisterSerializer
    permission_classes = (AllowAny,)


class AuthFacebookRegisterApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        if "token" in request.data and "username" in request.data:

            facebook = Facebook(request.data['token'])

            serializer = UserRsRegisterSerializer(data=facebook.get_profile(request.data['username']))
            serializer.is_valid(raise_exception=True)
            serializer.save()

            friends_id = facebook.get_friends()

            if friends_id:
                friends = User.objects.filter(idsn__in=friends_id)
                FacebookFriend.objects.bulk_create(
                    [FacebookFriend(user_id=serializer.data.get('id'), friend=x) for x in friends.all()]
                    +
                    [FacebookFriend(user=x, friend_id=serializer.data.get('id')) for x in friends.all()]
                )

            return Response({'token' :  serializer.data.get('token') }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthEmailUsernameCheckApiView(APIView):
    permission_classes = (AllowAny,)


    def post(self, request):
        print(request.data)

        if 'email' in request.data:
            if request.data['email']:
                if not User.objects.filter(email=request.data['email']).exists():
                    return Response(status=status.HTTP_200_OK)

        if 'username' in request.data:
            if request.data['username']:
                if not User.objects.filter(username=request.data['username']).exists():
                    return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AuthGeneratePresignedUrl(APIView): #type = photo ou video

    def post(self, request):
        if 'type' in request.data:
            if request.data['type'] in ("video", "photo"):
                s3 = boto3.client('s3')
                key = settings.MEDIAFILES_LOCATION+"/"+str(request.user.id)+"/"+request.data['type']+"/test.jpg"
                post = s3.generate_presigned_post(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key,
                    ExpiresIn=600
                )
                return Response(post, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
