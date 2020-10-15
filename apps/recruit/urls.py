from django.urls import re_path
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
    re_path(r'^recruits/{id}/$',views.One_Recruit_DetailView.as_view()),
    #7.7 添加职位访问次数
    re_path(r'^recruits/{id}/visit/$',views.Add_Recruit_VisitView.as_view()),
    # 7.8 收藏职位
    re_path(r'^recruits/{id}/collect/$',views.Collection_RecruitView.as_view()),
    # 7.8.1
    re_path(r'^recruits/{id}/collect/$',views.CancleCollection_RecruitView.as_view()),
    # re_path(r'^authorizations/$',obtain_jwt_token),



]
