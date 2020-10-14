from rest_framework import serializers
from .models import Channel, Article
from ..user.serializers import UserModelSerializer


class ChannelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name']


class LabelsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    label_name = serializers.StringRelatedField()


class ArticleSerializerForList(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)

    class Meta:
        model = Article
        fields = ("id", "title", "content", "createtime", "user", "collected_users", "collected", "image", "visits")


class ArticleSerializerForCreate(serializers.ModelSerializer):
    image = serializers.CharField(required=False, default='', allow_blank=True)

    class Meta:
        model = Article
        exclude = ('collected_users',)
