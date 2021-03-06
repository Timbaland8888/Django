#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: serializers.py
@time: 2019/6/9 22:40
@desc:
'''
# in useraccesscontrol/serializers.py

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # 导入DRF为我们提供的Token模型

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }  # we don't want to get back the password in response
        # which we ensure using extra_kwargs.

    def create(self, validated_data):
        # override the ModelSerializer method's create() to save the User instance.
        # we ensure that we set the password correctly using user.set_password,
        # rather than setting the raw password as the hash.
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user