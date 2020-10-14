from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models.query import QuerySet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .pagintions import MyPage
from ..question.models import Label
from rest_framework.response import Response


class ChannelViews(ModelViewSet):
    queryset = Channel.objects.filter()
    serializer_class = ChannelModelSerializer
    pagination_class = MyPage


class LabelsViews(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelsSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerForList
    pagination_class = MyPage

    # 获取请求方式
    def get_queryset(self):
        if self.action == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = None

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    # 新建文章
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
        except Exception:
            user = None

        if user and user.is_authenticated:
            request_params = request.data
            request_params['user'] = user.id
            serializer = ArticleSerializerForCreate(data=request_params)
            serializer.request = request
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            return Response({'success': True, 'message': '发布成功', 'articleid': article.id})
        else:
            return Response({'success': False, 'message': '请登录'}, status=401)

    # 文章列表
    def get_article_by_channel(self, request, pk):
        if pk == "-1":
            articles = self.get_queryset()
        else:
            channel = Channel.objects.get(id=pk)
            articles = self.get_queryset().filter(channel=channel)

        page = self.paginate_queryset(articles)
        if page is not None:
            s = ArticleSerializerForList(page, many=True)
            return self.get_paginated_response(s.data)
        else:
            s = ArticleSerializerForList(instance=articles, many=True)
            return Response(s.data)

    # def Article_Collect(self, request, pk):
    #     try:
    #         use = request.use
    #     except Exception:
    #         use = None
