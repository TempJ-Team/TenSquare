from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^channels/$', views.ChannelViews.as_view({'get': 'list'})),  # 频道列表
    re_path(r'^labels/$', views.LabelsViews.as_view({'get': 'list'})),  # 获取标签
    re_path(r'^article/$', views.ArticleViewSet.as_view({'post': 'create'})),  # 发布文章
    re_path(r'^article/(?P<pk>-?[1-9]\d*)/channel/$', views.ArticleViewSet.as_view({'get': 'get_article_by_channel'})),  # 文章列表
]
