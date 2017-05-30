from rest_framework import serializers
from ..models import Spitch


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


class SpitchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spitch
        fields = ("id", "user", "ask", "clip_uploaded", "clip_total", "created")