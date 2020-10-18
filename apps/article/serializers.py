from rest_framework import serializers
from .models import Channel, Article, Comment
from apps.user.serializers import UserModelSerializer
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ArticleIndex
from apps.user.serializers import UserModelSerializer
from haystack.views import search_view_factory


class ChannelsSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.StringRelatedField()


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


class CommentModelSerializer2(serializers.ModelSerializer):
    subs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

# 递归实现无限层级回复
class RecursiveCommentField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentModelSerializer(serializers.ModelSerializer):
    subs = RecursiveCommentField(many=True, read_only=True)
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = CommentModelSerializer(many=True, read_only=True)
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleIndexSerializer(HaystackSerializer):
    """
    Article索引结果数据序列化器
    """

    class Meta:
        index_classes = [ArticleIndex]
        fields = ('text', 'id', 'title', 'content', 'createtime')


class ArticleModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    user_id = serializers.IntegerField(label='用户id', write_only=True)
    collected_users = StringRelatedField(label='收藏用户', read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'
