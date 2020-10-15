from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Spit
from rest_framework_jwt.utils import jwt_payload_handler,jwt_encode_handler


class SpitSimpleSerializer(serializers.ModelSerializer):
    # comment = serializers.IntegerField(required=False)
    # parent = serializers.StringRelatedField()
    class Meta:
        model = Spit
        fields ='__all__'

    # def create(self, validated_data):
    #     #1、新增一个 吐槽，parent设置为路径参数id的吐槽
    #     #2、根据路径参数id获取被吐槽的对象，把coment+1


class SpitCommentSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = Spit
        fields ='__all__'


