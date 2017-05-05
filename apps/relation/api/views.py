# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from ..models import Follow, FacebookFriend
from apps.authentication.models import User
from apps.authentication.facebook import Facebook
from apps.core.states import FollowUser



class FacebookFriendListApiView(generics.ListAPIView):
    serializer_class = ListFacebookFriendSerializer

    def get_queryset(self):
        return FacebookFriend.objects.filter(user = self.request.user)



class FollowCreateApiView(generics.CreateAPIView):
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        FollowUser(self.request.user.id).follow(serializer.data['follow'])
        # FacebookFriend.objects.filter(user=self.request.user, friend_id=serializer.data.get('follow')).update(follow=True)



class FollowAllCreateApiView(APIView):

    def post(self, request, format=None):
        ids = self.request.user.facebook_friends\
            .exclude(friend_id__in=self.request.user.follows.values_list('follow_id', flat=True))\
            .values_list('friend_id', flat=True)

        if ids:
            Follow.objects.bulk_create(
                [Follow(user=self.request.user, follow_id=x) for x in ids]
            )
            FollowUser(self.request.user.id).follow(list(ids))

        return Response(status=status.HTTP_200_OK)



class GenerateListFacebook(APIView):

    def post(self, request, format=None):
        serializer = GenerateFacebookList(data=request.data)
        serializer.is_valid(raise_exception=True)

        facebook = Facebook(serializer.validated_data['token'])

        self.request.user.idsn = facebook.get_id()
        self.request.user.save()

        friends_id = facebook.get_friends()

        if friends_id:
            friends = User.objects.filter(idsn__in=friends_id)

            FacebookFriend.objects.bulk_create(
                [FacebookFriend(user=self.request.user, friend=x) for x in friends.all()]
                +
                [FacebookFriend(user=x, friend=self.request.user) for x in friends.all()]
            )

        return Response({'token' : self.request.user.get_token()}, status=status.HTTP_200_OK)


