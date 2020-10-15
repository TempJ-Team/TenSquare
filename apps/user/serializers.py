from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *
from apps.question.serializers import LablesModelSerializer, QuestionsModelSerializer, ReplySerializerForList
from apps.recruit.serializers import RecruitModelSerialier, EnterpriseModelSerializer


# 用户注册
class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

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

    # TODO：这里可能有些不需要 many=True后续再改
    # ==> question
    questions = QuestionsModelSerializer(many=True, read_only=True)
    replies = ReplySerializerForList(many=True, read_only=True)
    labels = LablesModelSerializer(many=True, read_only=True)
    # ==> artical
    collected_articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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














