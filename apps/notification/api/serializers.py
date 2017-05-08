from rest_framework import serializers


class ItemNotificationSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    user = serializers.DictField(default=None)
    obj = serializers.DictField(default=None)
    timestamp = serializers.IntegerField()

class NotificationSerializer(serializers.Serializer):
    items = ItemNotificationSerializer(many=True)
    next = serializers.CharField(default=None)
