from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .serializers import *

# 推荐职位7.1
class Recommend_RecruitView(ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Recommend_RecruitModelSerializer
# #
# class RecruitView(ListAPIView):
#     queryset = Recruit.objects.all()
#     serializers_class = RecruitModelSerialier


# 热门城市7.4
class Hot_CityView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = Hot_CityModelSerialier





