# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import uuid
import requests

from rest_framework import serializers

from ..models import User



from django.core.files.base import ContentFile


class UrlImageField(serializers.ImageField):

    def to_internal_value(self, data):
        img = requests.get(data)
        data = ContentFile( img )
        return super(UrlImageField, self).to_internal_value(data)



class UserRsRegisterSerialier(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True)
    photo = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'token', 'photo']
        read_only_fields = ('token','id')
        extra_kwargs = {
            'first_name': {'required': False, 'write_only': True},
            'last_name': {'required': False, 'write_only': True},
            'username': {'write_only': True},
            'email': {'write_only': True},
        }

    def create(self, validated_data):
        url = validated_data.get('photo')
        del validated_data['photo']
        user = User.objects.create_user(**validated_data)

        img = requests.get(url)
        print(url.split('/')[-1])
        user.photo.save(url.split('/')[-1], ContentFile(img.content), save=True)

        return {'token' : user.get_token() }




class UserEmailRegisterSerialier(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True)
    url_photo = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'username', 'token', 'url_photo']
        read_only_fields = ('token','id')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'write_only': True},
            'last_name': {'required': False, 'write_only': True},
            'username': {'write_only': True},
            'email': {'write_only': True},
        }

    def create(self, validated_data):
        print (validated_data.get('url_photo'))

        # user = User.objects.create_user(**validated_data)

        #user.uuid = str(user.id)+str(uuid.uuid4()).replace("-", "")[:10]
        #user.save()



        return {'token' : token}