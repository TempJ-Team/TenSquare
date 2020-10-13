from django.urls import path, re_path
from . import views

urlpatterns = [
    # 展示活动列表
    path('', views.Gatherings.as_view()),
    # 活动详情
    re_path(r'^(?P<pk>[^/.]+)/$', views.GatheringView.as_view()),
    # 报名活动
    re_path(r"^(?P<pk>[^/.]+)/join/$", views.GatherJoinView.as_view()),

]
