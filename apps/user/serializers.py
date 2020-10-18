from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *

from apps.question.serializers import LablesModelSerializer, QuestionsModelSerializer, ReplySerializerForList
from apps.recruit.serializers import RecruitModelSerialier, EnterpriseModelSerializer
from apps.article.models import Article


# 用户注册
class UserModelSerializer(serializers.ModelSerializer):
    fans = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'

    # 密码要加密
    def validate(self, attrs):
        raw_password = attrs.pop('password')
        secret_password = make_password(raw_password)
        attrs['password'] = secret_password

        return attrs


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

# 用户个人中心
class UserInfoSerializer(serializers.ModelSerializer):
    '''用户信息'''
    username = serializers.CharField(read_only=True)

    # TODO：这里可能有些不需要 read_only=True后续再改
    # ==> question
    questions = QuestionsModelSerializer(many=True, read_only=True)
    replies = ReplySerializerForList(many=True, read_only=True)
    labels = LablesModelSerializer(many=True, read_only=True)
    # ==> artical
    collected_articles = ArticleDetailSerializer(many=True, read_only=True)
    # ==> recruit
    enterpises = EnterpriseModelSerializer(many=True, read_only=True)
    recruits = RecruitModelSerialier(many=True, read_only=True)

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

            'labels',
            'questions',
            # 'answer_question',  # 不存在的字段？ 应该是replies?
            'replies',
            'collected_articles',
            'enterpises',
            'recruits',
        ]

# 修改用户标签
class ChangeLabelModelSerializer(serializers.ModelSerializer):
    labels = LablesModelSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'labels'
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














