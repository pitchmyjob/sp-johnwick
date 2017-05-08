import re

from rest_framework import serializers
from ..models import Ask, Tag, Asktag
from apps.core.states import AskUser
from apps.authentication.models import User

class AskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ask
        fields = ('text',)
        extra_kwargs = { 'text': {"min_length" : 3} }

    def create(self, validated_data):
        instance = super(AskCreateSerializer, self).create(validated_data)
        hashtags = set(map(str.lower, re.findall(r"#(\w+)", validated_data['text'])))

        for hash in hashtags:
            tag, created = Tag.objects.get_or_create(tag=hash.lower())
            Asktag.objects.create(tag=tag, ask=instance)

        AskUser(instance.user.id).ask(instance, hashtags)

        return instance

class TrendTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag')


class UserAskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo")

class AskListSerializer(serializers.ModelSerializer):
    user = UserAskSerializer()
    class Meta:
        model = Ask
        fields = ('text', 'id', 'user', 'created')