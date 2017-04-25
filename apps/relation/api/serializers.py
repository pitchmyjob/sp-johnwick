# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers
from ..models import FacebookFriend, Follow


class ListFacebookFriendSerializer(serializers.ModelSerializer):

    id = serializers.StringRelatedField(source='friend.id')
    username = serializers.StringRelatedField(source='friend.username')
    first_name = serializers.StringRelatedField(source='friend.first_name')
    last_name = serializers.StringRelatedField(source='friend.last_name')
    photo = serializers.StringRelatedField(source='friend.photo.url')
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.user.follows.filter(follow=obj.friend).exists()
        # return Follow.objects.filter(user=obj.user, follow=obj.follow).exists()

    class Meta:
        model = FacebookFriend
        fields = ('id', 'username', 'first_name', 'last_name', 'photo', 'follow')



class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('follow', )


class GenerateFacebookList(serializers.Serializer):
    token = serializers.CharField(required=True)