# 模型类
from django.db import models


class Users(models.Model):
    """用户模型类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'


# 序列化器
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re



class UserModelSerializers(serializers.ModelSerializer):
    username = serializers.CharField(min_length=8, max_length=20, required=True)
    password = serializers.CharField(min_length=5, max_length=20, required=True, write_only=True)
    mobile = serializers.CharField(max_length=11, required=True)

    class Meta:
        model = Users
        fields = '__all__'

    def validate(self, attrs):
        mobile = attrs['mobile']
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError("手机号码格式不正确！")
        raw_password = attrs.pop('password')
        secret_password = make_password(raw_password)
        attrs['password'] = secret_password
        return attrs


# 视图
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class UserCreateView(CreateModelMixin, GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UserModelSerializers
