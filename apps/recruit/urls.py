from django.urls import re_path, path
from . import views

urlpatterns = [
    # 7.1推荐职位
    re_path(r'^recruits/search/recommend/$', views.Recommend_RecruitView.as_view()),
    # re_path(r'^recruits/search/recommend/$',views.RecruitView.as_view()),
    # 7.4热门城市
    re_path(r'^city/hotlist/$', views.Hot_CityView.as_view()),


    # 热门企业
    path('enterprise/search/hotlist/', views.HotCompanyView.as_view()),
    # 增加企业访问次数
    path('enterprise/<int:id>/visit/', views.CompanyInfoView.as_view()),
    # 收藏公司
    path('enterprise/<int:id>/collect/', views.CollectCompanyView.as_view()),
    # 取消收藏公司
    path('enterprise/<int:id>/cancelcollect/', views.CancleCollectCompanyView.as_view()),
    # 企业详情
    path('enterprise/<int:id>/', views.CompanyInfoView.as_view()),
    # 最新职位
    path('recruits/search/latest/', views.LastestRecruitView.as_view()),
    # 搜索职位
    path('recruits/search/city/keyword/', views.LastestRecruitView.as_view()),
]
