from django.shortcuts import render
from haystack.views import SearchView

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView, GenericAPIView
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *

# 推荐职位7.1
class Recommend_RecruitView(ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Recommend_RecruitModelSerializer

#最新职位7.2
class The_Latest_JobView(ListAPIView):
    queryset = Recruit.objects.all().order_by('-createtime')
    serializer_class = One_The_Latest_JobModelSerialiazer

# 热门企业7.3
class Hot_EnterpriseView(ListAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = One_Hot_EnterpriseModelSerializer

# 热门城市7.4
class Hot_CityView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = Hot_CityModelSerialier


#
# #搜索职位7.5
# class Search_JobsView(CreateAPIView,SearchView):
#     queryset = Recruit.objects.all()
#     serializer_class = One_Search_JobsModelSerializer
#
#     def create_response(self):
#
#         context = self.get_context()
#
#         ret_List=[]
#         for result in context['page'].object_list:
#             recruit = result.object
#             ret_List.append({
#                 'id':recruit.id,
#                 'jobname':recruit.jobname,
#                 'salary':recruit.salary,
#                 'condition':recruit.condition,
#                 'education':recruit.condition,
#                 'type':recruit.type,
#                 'city':recruit.city,
#                 'createtime':recruit.createtime,
#                 'enterprise':recruit.enterprise,
#                 'labels':recruit.labels,
#             })
#
#
#         return JsonResponse(ret_List,safe=False)


# 7.6职位详情
class One_Recruit_DetailView(ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = One_Recruit_DetailModdelSerializer


# 7.7增加职位访问次数
class Add_Recruit_VisitView(UpdateAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Add_Recruit_VisitSerializer

    # def update(self, request, *args, **kwargs):
    #     pass

    def put(self, request,id,*args, **kwargs):
        _data = self.queryset.get(pk = id)
        _data.visits += 1
        _data.save()



        return Response({
            'message':"更新成功",
            'success':True
        },status=status.HTTP_201_CREATED)


# 7.8收藏职位
class Collection_RecruitView(GenericAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Collection_RecruitSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):

        return self.request.user

    def post(self, request,id, *args, **kwargs):

        recruit = self.queryset().get(pk=id)
        user = self.get_object()

        recruit.users.add(user)
        recruit.save()

        return Response({
            'message': "收藏成功",
            'success': True
        }, status=status.HTTP_201_CREATED)


class CancleCollection_RecruitView(GenericAPIView):

    queryset = Recruit.objects.all()
    serializer_class =  Collection_RecruitSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):

        return self.request.user


    def post(self, request,id, *args, **kwargs):

        recruit = self.queryset().get(pk=id)
        user = self.get_object()

        recruit.users.remove(user)
        recruit.save()


        return Response({
            'message':'取消收藏成功',
            'success':True
        })














