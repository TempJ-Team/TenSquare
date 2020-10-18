from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models.query import QuerySet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .pagintions import MyPage
from ..question.models import Label
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from drf_haystack.viewsets import HaystackViewSet

class ChannelViews(ModelViewSet):
    queryset = Channel.objects.filter()
    serializer_class = ChannelsSerializers
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


class ArticleCollectView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user = request.user
        try:

            article = Article.objects.get(id=id)
        except Exception as e:
            return Response(status=404,
                            data={
                                'errmsg': 'article_id错误'
                            })
        # 判断是否收藏
        collected_users = article.collected_users.all()
        if user in collected_users:
            article.collected_users.remove(user)
        else:
            article.collected_users.add(user)
        # 返回响应
        return Response({
            'message': "ok",
            'success': True
        })


# 文章详情
class ArticleDetailView(APIView):

    def get(self, request, id):
        try:
            article = Article.objects.get(id=id)

        except Exception as e:
            return Response(status=404,
                            data={'errmsg': 'article_id错误'})
        serializer = ArticleDetailSerializer(instance=article)
        return Response(serializer.data)


class ArticleSearchViewSet(HaystackViewSet):
    """
    Article搜索
    """
    index_models = [Article]
    serializer_class = ArticleIndexSerializer
    pagination_class = MyPage








class SearchArticleView(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        # 获取搜索内容
        text = self.request.query_params.get('text')
        # 查询内容
        _info = Article.objects.filter(title__contains=text)
        return _info


# 评论文章
class PubCommentView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer2
    lookup_field = 'id'
    lookup_url_kwarg = lookup_field
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, id):
        article = Article.objects.all().get(id=id)
        user = self.request.user
        _data = request.data
        _data['user'] = user.id
        _data['article'] = article.id

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        serializer.save()
        article.comment_count += 1
        article.save()

        return Response({
            'success': 'true',
            'message': '评论发表成功'
        })
