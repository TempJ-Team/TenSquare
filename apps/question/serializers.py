from rest_framework import serializers
from .models import *
from apps.article.models import Article
from apps.recruit.models import Recruit
from apps.recruit.serializers import EnterpriseModelSerializer

# 个人提问
class LablesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'

class QuestionsModelSerializer(serializers.ModelSerializer):
    labels = LablesModelSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
#所有标签
class  LabelAllModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'

#最新问题展示
class QusetionModelSerializer(serializers.ModelSerializer):
    labels =serializers.StringRelatedField(many=True)
    class Meta:
        model = Question
        fields ='__all__'

#最多回答问题展示
class LabelHotModelSerializer(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)
    class Meta:
        model = Question
        fields = '__all__'

#等待回答问题展示
class LabelWaitModelSerializer(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)
    class Meta:
        model = Question
        fields = '__all__'

#发布问题
class ReleasequestionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Question
        fields = '__all__'

#问题详情

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ReplySerializerForSubAndParent(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count","unuseful_count","user"]

class ReplySerializerForList(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    subs = ReplySerializerForSubAndParent(read_only=True, many=True)
    parent = ReplySerializerForSubAndParent(read_only=True)

    class Meta:
        model = Reply
        fields = '__all__'

class QuestionDetailsSerialzer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True, many=True)
    # replies = ReplySerializerForList(read_only=True, many=True)
    comment_question = ReplySerializerForList(read_only=True, many=True)
    comment_reply = ReplySerializerForList(read_only=True, many=True)
    answer_question = ReplySerializerForList(read_only=True, many=True)

    class   Meta:
        model  =  Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits","content","comment_question","comment_reply","answer_question"]

#回答问题
class ReplyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['problem','content','type','parent','user']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

#标签详情
class QuestionSerializerforTagsDetails(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = '__all__'

class ArticleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

class RecruitModelSerialier(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer()
    class Meta:
        model = Recruit
        fields = '__all__'

class TagsDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializerforTagsDetails(many=True)
    articles = ArticleModelSerializer(many=True)
    labelRecruits = RecruitModelSerialier(many=True)
    class Meta:
        model = Label
        fields = '__all__'
