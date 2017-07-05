from rest_framework import serializers
from ..models import Spitch
from apps.authentication.models import User
from apps.ask.models import Ask


class InitializeSpitchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spitch
        read_only = ("id", )
        fields = ("id", "ask")


class EndSpitchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spitch
        fields = ("clip_total",)
        extra_kwargs = {
            'clip_total': {'required': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "photo")

class AskSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Ask
        fields = ("id", "text", "user")


class SpitchSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ask = AskSerializer()

    class Meta:
        model = Spitch
        fields = ("id", "user", "ask", "video", "spitch", "created")