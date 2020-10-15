from django.urls import re_path, path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('articles/search', views.ArticleSearchViewSet, basename='articles_search')

urlpatterns = [
    re_path(r'^channels/$', views.ChannelViews.as_view({'get': 'list'})),  # 频道列表
    re_path(r'^labels/$', views.LabelsViews.as_view({'get': 'list'})),  # 获取标签
    re_path(r'^article/(?P<id>\d+)/$', views.ArticleDetailView.as_view()),  # 文章详情
    re_path(r'^article/$', views.ArticleViewSet.as_view({'post': 'create'})),  # 发布文章
    re_path(r'^article/(?P<pk>-?[1-9]\d*)/channel/$', views.ArticleViewSet.as_view({'get': 'get_article_by_channel'})),
    # 文章列表
    re_path(r'^article/(?P<id>\d+)/collect/$', views.ArticleCollectView.as_view()),  # 收藏文章
    # re_path(r'^articles/search/$', views.SearchArticleView.as_view({'get': 'list'})),
    # 评论文章
    path('article/<int:id>/publish_comment/', views.PubCommentView.as_view()),
]

urlpatterns += router.urls
