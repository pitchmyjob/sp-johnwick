# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework_jwt.settings import api_settings
from rest_framework import serializers

from ..models import User


class UserRegisterSerialier(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'username', 'token']
        read_only_fields = ('token','id')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'write_only': True},
            'last_name': {'required': False, 'write_only': True},
            'username': {'write_only': True},
            'email': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return {'token' : token}