from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Spit
from apps.user.models import User
from rest_framework_jwt.utils import jwt_payload_handler,jwt_encode_handler


class SpitSimpleSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(allow_null=True)
    # comment = serializers.IntegerField(required=False)
    # parent = serializers.StringRelatedField()
    # collected_users = serializers.ManyRelatedField(allow_null=True)
    # hasthumbup_users = serializers.ManyRelatedField(allow_null=True)
    class Meta:
        model = Spit
        fields =[
            'id',
            'content',
            'publishtime',
            'userid',
            'nickname',
            'visits',
            'thumbup',
            'comment',
            'avatar',
            'parent',
            'hasthumbup',
            'collected',
        ]

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id']

class SpitCollectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spit
        fields = [
            'id',
            'collected_users',
            'collected',
        ]

class SpithasthumbupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spit
        fields = [
            'id',
            'hasthumbup_users',
            'hasthumbup',
        ]
    # def create(self, validated_data):
    #     #1、新增一个 吐槽，parent设置为路径参数id的吐槽
    #     #2、根据路径参数id获取被吐槽的对象，把coment+1


class SpitCommentSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = Spit
        fields ='__all__'


