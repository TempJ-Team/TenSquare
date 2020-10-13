from django.urls import re_path
from . import views

urlpatterns = [
    # 7.1推荐职位
    re_path(r'^recruits/search/recommend/$',views.Recommend_RecruitView.as_view()),
    # re_path(r'^recruits/search/recommend/$',views.RecruitView.as_view()),
    # 7.4热门城市
    re_path(r'^city/hotlist/$',views.Hot_CityView.as_view()),



]
