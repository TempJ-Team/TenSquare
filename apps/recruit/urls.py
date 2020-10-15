'''
Descripition: 
Version: 
Author: SmartFox97
Date: 2020-10-14 00:46:57
LastEditors: SmartFox97
LastEditTime: 2020-10-15 16:35:17
'''
from django.urls import re_path, path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 7.1推荐职位
    re_path(r'^recruits/search/recommend/$',views.Recommend_RecruitView.as_view()),
    # 7.2最新职位
    re_path(r'^recruits/search/latest/$',views.The_Latest_JobView.as_view()),
    # 7.3热门企业
    re_path(r'^enterprise/search/hotlist/$',views.Hot_EnterpriseView.as_view()),
    # 7.4热门城市
    re_path(r'^city/hotlist/$',views.Hot_CityView.as_view()),
    # # # 7.5职位搜索
    # re_path(r'^recruits/search/city/keyword/$',views.Search_JobsView()),
    # 7.6职位详情
    path('recruits/<int:pk>/',views.One_Recruit_DetailView.as_view()),
    #7.7 添加职位访问次数
    path('recruits/<int:id>/visit/',views.Add_Recruit_VisitView.as_view()),
    # 7.8 收藏职位
    path('recruits/<int:id>/collect/',views.Collection_RecruitView.as_view()),
    # 7.8.1
    path('recruits/<int:id>/collect/',views.CancleCollection_RecruitView.as_view()),
    # re_path(r'^authorizations/$',obtain_jwt_token),



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
