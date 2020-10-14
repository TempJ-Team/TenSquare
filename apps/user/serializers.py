from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from  rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from apps.question.serializers import *
from apps.article.serializers import *
from apps.recruit.serializers import *


# 用户注册
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'mobile',
        ]

    # 密码要加密
    def validate(self, attrs):
        raw_password = attrs.pop('password')
        secret_password = make_password(raw_password)
        attrs['password'] = secret_password

        return attrs


# 用户个人中心
class UserInfoSerializer(serializers.ModelSerializer):
    '''用户信息'''
    username = serializers.CharField(read_only=True)
    # questions = QuestionsModelSerializer(many=True)
    # lables = QuestionsModelSerializer(many=True)
    # collected_articles = ArticleModelSerializer(many=True)
    # enterpises = EnterpriseModelSerializer(many=True)
    # recruits = RecruitModelSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile',
            'realname',
            'birthday',
            'sex',
            'avatar',
            'website',
            'city',
            'email',
            'address',
            # 'lables',
            # 'questions',
            # # 'answer_question',  # 不存在的字段？
            # 'collected_articles',
            # 'enterpises',
            # 'recruits',
        ]


# 修改用户密码
class ChangePasswordModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def validate(self, attrs):
        raw_password = attrs.pop('password')
        secret_password = make_password(raw_password)
        attrs['password'] = secret_password

        return attrs


# 关注用户/取消关注












