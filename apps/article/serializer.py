from rest_framework import serializers
from .models import Channel, Article


class ChannelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name']


class ArticleSerializerForCreate(serializers.ModelSerializer):
    image = serializers.CharField(required=False, default='', allow_blank=True)

    class Meta:
        model = Article
        exclude = ('collected_users',)
