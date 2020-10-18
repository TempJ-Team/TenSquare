from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django_redis import get_redis_connection


# 1,2
class LabelView(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelAllModelSerializer

    @action(methods=['get'], detail=False)
    def latest(self, request, *args, **kwargs):
        user = self.request.user
        label_name = user.labels.all()
        serializer = self.get_serializer(instance=label_name, many=True)
        return Response(data=serializer.data)


# 3
#3
class QuestionView(ModelViewSet):
    serializer_class = QusetionModelSerializer
    def list(self, request, id):
        if id == '-1':
            queryset = Question.objects.all().order_by('-createtime')
        else:
            label = Label.objects.get(pk = id)
            queryset = label.questions.all().order_by('-createtime')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 4
class HotquestionView(ModelViewSet):
    serializer_class = QusetionModelSerializer
    def list(self, request, id):
        if id == '-1':
            queryset = Question.objects.all().order_by('-reply')
        else:
            label = Label.objects.get(pk = id)
            queryset = label.questions.all().order_by('-reply').order_by('-createtime')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#5
class WiatquestionView(ModelViewSet):
    serializer_class = QusetionModelSerializer

    def list(self, request, id):
        if id == '-1':
            queryset = Question.objects.all().filter(reply=0)
        else:
            label = Label.objects.get(pk=id)
            queryset = label.questions.all().filter(reply=0).order_by('createtime')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 6
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


# 7
class QuestiondetailsView(ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Question.objects.all()
    serializer_class = QuestionDetailsSerialzer

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


# 8
class UsefulQuestionView(GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QusetionModelSerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('Q_collected')
        user = self.request.user
        if not conn.get('Q_Useful_%s_%s' % (user.id, pk)):
            request_data = self.get_queryset().get(pk=pk)
            request_data.useful_count = request_data.useful_count + 1
            request_data.save()
            conn.delete('Q_unUseful_%s_%s' % (user.id, pk))
            conn.set('Q_Useful_%s_%s' % (user.id, pk),1)
            return Response({
                'success': True,
                'message': '不错的问题'
            })
        else:
            return Response({
                'success': False,
                'message': '请勿重复点赞'
            })


# 9
class UnusefulQuestionView(GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QusetionModelSerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('Q_collected')
        user = self.request.user

        if not conn.get('Q_unUseful_%s_%s' % (user.id, pk)):
            request_data = self.get_queryset().get(pk=pk)
            request_data.useful_count = request_data.useful_count - 1
            request_data.save()
            conn.delete('Q_Useful_%s_%s' % (user.id, pk))
            conn.set('Q_unUseful_%s_%s' % (user.id, pk), 1)
            return Response({
                'success': 'true',
                'message': '垃圾问题'
            })
        else:
            return Response({
                'success': False,
                'message': '请勿重复踩别人'
            })


# 10
class ReplyView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Reply.objects.all()
    serializer_class = ReplyQuestionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        problem = instance.problem
        problem.reply += 1
        problem.save()

    def create(self, request, *args, **kwargs):
        _data = request.data

        _data['user'] = self.request.user.id
        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 11
class UsefulQView(GenericAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('A_collected')
        user = self.request.user

        if not conn.get('A_Useful_%s_%s' % (user.id, pk)):
            request_data = self.get_queryset().get(pk=pk)
            request_data.useful_count += 1
            request_data.save()

            conn.delete('A_unUseful_%s_%s' % (user.id, pk))
            conn.set('A_Useful_%s_%s' % (user.id, pk), 1)
            return Response({
                'success': True,
                'message': '点赞成功'
            })
        else:
            return Response({
                'success': False,
                'message': '请勿重复点赞'
            })

# 12
class UnusefulQView(GenericAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def put(self, request, pk, *args, **kwargs):
        conn = get_redis_connection('A_collected')
        user = self.request.user

        if not conn.get('A_unUseful_%s_%s' % (user.id, pk)):
            request_data = self.get_queryset().get(pk=pk)
            request_data.useful_count -= 1
            request_data.save()

            conn.delete('A_Useful_%s_%s' % (user.id, pk))
            conn.set('A_unUseful_%s_%s' % (user.id, pk), 1)
            return Response({
                'success': 'true',
                'message': '点踩成功'
            })
        else:
            return Response({
                'success': False,
                'message': '请勿重复踩别人'
            })


# 13 关注标签
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
            'success': True,
            'message': '关注成功'
        })


# 14 取消关注标签
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
            'success': 'true',
            'message': '取消关注成功'
        })


# 15
class TagsView(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = TagsDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 16
class LabelFullView(ListAPIView):

    def get(self, request):
        labels = Label.objects.all()
        serializer = LabelAllModelSerializer(labels, many=True)
        return Response(serializer.data)
