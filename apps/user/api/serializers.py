from rest_framework import serializers
from apps.authentication.models import User
from apps.ask.models import Ask


class UserAskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ask
        fields = ("id", "text", "created")


class UserMeSerializer(serializers.ModelSerializer):

    datas = serializers.SerializerMethodField()
    asks = serializers.SerializerMethodField()
    spitchs = serializers.SerializerMethodField()

    def get_spitchs(self, obj):
        return []

    def get_asks(self, obj):
        return UserAskSerializer(instance=obj.asks.order_by('-created'), many=True).data

    def get_datas(self, obj):
        return {
            "videos" : 0,
            "follows" : obj.follows.count(),
            "followers" : obj.followers.count()
        }

    class Meta:
        model = User
        fields = ("id", "title", "datas", "asks", "spitchs")


class UserSerializer(UserMeSerializer):

    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        return obj.followers.filter(user=self.context['request'].user).exists()

    class Meta:
        model = User
        fields  = ("id", "username", "photo", "title", "follow", "datas", "asks", "spitchs")


