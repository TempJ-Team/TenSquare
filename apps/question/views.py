from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView,GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django_redis import get_redis_connection



#1,2
class LabelView(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelAllModelSerializer

    @action(methods=['get'], detail=False)
    def latest(self,request,*args, **kwargs):
        user = self.request.user
        label_name = user.labels.all()
        serializer = self.get_serializer(instance =label_name,many = True)
        return Response(data=serializer.data)

#3
class QuestionView(ListAPIView):
    queryset = Question.objects.all().order_by('-createtime')
    serializer_class = QusetionModelSerializer

# 4
class HotquestionView(ListAPIView):
    queryset = Question.objects.all().order_by('-reply')
    serializer_class = LabelHotModelSerializer

#5
class WiatquestionView(ListAPIView):
    queryset = Question.objects.all().filter(reply=0).order_by('createtime')
    serializer_class = LabelHotModelSerializer

#6
class ReleasequestionView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def create(self, request, *args, **kwargs):
        _data = request.data
        _data['user_id'] = request.user.id
        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        return ReleasequestionSerializer

    def get_queryset(self):
        return Question.objects.all()

#7
class QuestiondetailsView(ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Question.objects.all()
    serializer_class =QuestionDetailsSerialzer

    def retrieve(self, request, pk):
        question = self.get_object()
        question.visits += 1
        question.save()
        replies = question.replies.all()
        question.comment_question = []
        question.answer_question = []

        for item in replies:
            if item.type == 0:
                question.comment_question.append(item)
            elif item.type == 2:
                question.answer_question.append(item)

        s = QuestionDetailsSerialzer(instance=question)
        return Response(s.data)

#8
class UsefulQuestionView(GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QusetionModelSerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('Q_collected')
        user = self.request.user
        U_Q_collected = conn.get('Q_collected_%s' % user.id)
        if pk not in U_Q_collected:
            request_data = self.get_queryset().get(pk=pk)
            request_data.useful_count = request_data.useful_count + 1
            request_data.save()
            return Response({
                'success': True,
                'message': '有用问题+1'
            })
        else:
            return Response({
                'success': False,
                'message':'请勿重复点赞'
            })

#9
class UnusefulQuestionView(GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QusetionModelSerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('Q_collected')
        user = self.request.user
        request_data = self.get_queryset().get(pk=pk)
        request_data.useful_count = request_data.useful_count - 1
        request_data.save()
        return Response({
            'success': 'true',
            'message': '有用问题-1'
        })
#10
class ReplyView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Reply.objects.all()
    serializer_class = ReplyQuestionSerializer

    def create(self, request, *args, **kwargs):
        _data = request.data

        _data['user'] = self.request.user.id
        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#11
class UsefulQView(GenericAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('A_collected')
        user = self.request.user
        request_data = self.get_queryset().get(pk=pk)
        request_data.useful_count += 1
        request_data.save()
        return Response({
                'success': True,
                'message': '有用问题+1'
            })

#12
class UnusefulQView(GenericAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('A_collected')
        user = self.request.user
        request_data = self.get_queryset().get(pk=pk)
        request_data.useful_count -= 1
        request_data.save()
        return Response({
                'success': True,
                'message': '没用问题+1'
            })


#13 关注标签
class AttentionstagsView(GenericAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelAllModelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def put(self, request, pk, *args, **kwargs):
        tags = self.get_queryset().get(pk=pk)
        user = self.request.user
        print(user)

        tags.users.add(user)

        return Response({
            'success':True,
            'message':'关注成功'
        })


#14 取消关注标签
class AttentiontagsView(GenericAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelAllModelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def put(self, request, pk, *args, **kwargs):
        tags = self.get_queryset().get(pk=pk)
        user = self.request.user

        tags.users.remove(user)

        return Response({
            'success':'true',
            'message':'取消关注成功'
        })

#15
class TagsView(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = TagsDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#16
class LabelFullView(ListAPIView):

    def get(self, request):
        labels = Label.objects.all()
        serializer = LabelAllModelSerializer(labels, many=True)
        return Response(serializer.data)


















