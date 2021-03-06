from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *


# 推荐职位7.1
class Recommend_RecruitView(ListAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Recommend_RecruitModelSerializer


# 最新职位7.2
class The_Latest_JobView(ListAPIView):
    queryset = Recruit.objects.all().order_by('-createtime')
    serializer_class = One_The_Latest_JobModelSerialiazer


# 热门企业7.3
class Hot_EnterpriseView(ListAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = One_Hot_EnterpriseModelSerializer


# 热门城市7.4
class Hot_CityView(ListAPIView):
    queryset = City.objects.all().filter(ishot=True)
    serializer_class = Hot_CityModelSerialier

# 7.6职位详情
class One_Recruit_DetailView(RetrieveAPIView):
    queryset = Recruit.objects.all()
    serializer_class = One_Recruit_DetailModdelSerializer


# 7.7增加职位访问次数
class Add_Recruit_VisitView(UpdateAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Add_Recruit_VisitSerializer

    def put(self, request, id, *args, **kwargs):
        _data = self.queryset.get(pk=id)
        _data.visits += 1
        _data.save()

        return Response({
            'message': "更新成功",
            'success': True
        }, status=status.HTTP_201_CREATED)


# 7.8收藏职位
class Collection_RecruitView(GenericAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Collection_RecruitSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        return self.request.user

    def post(self, request, id, *args, **kwargs):
        recruit = self.get_queryset().get(pk=id)
        user = self.get_object()

        recruit.users.add(user)
        recruit.save()

        return Response({
            'message': "收藏成功",
            'success': True
        }, status=status.HTTP_201_CREATED)


class CancleCollection_RecruitView(GenericAPIView):
    queryset = Recruit.objects.all()
    serializer_class = Collection_RecruitSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        return self.request.user

    def post(self, request, id, *args, **kwargs):
        recruit = self.get_queryset().get(pk=id)
        user = self.get_object()

        recruit.users.remove(user)
        recruit.save()

        return Response({
            'message': '取消收藏成功',
            'success': True
        })


# 热门企业
class HotCompanyView(ListAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseModelSerializer


# 企业详情/增加访问次数
class CompanyInfoView(RetrieveAPIView, GenericAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseModelSerializer
    lookup_field = 'id'
    lookup_url_kwarg = lookup_field

    def put(self, request, *args, **kwargs):
        enterprise = self.get_object()
        enterprise.visits += 1
        enterprise.save()
        return Response({
            'success': 'true',
            'message': '更新成功'
        })


# 收藏公司
class CollectCompanyView(GenericAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseModelSerializer
    lookup_field = 'id'
    lookup_url_kwarg = lookup_field
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, id, *args, **kwargs):
        enterprise = self.get_queryset().get(id=id)
        user = self.get_object()

        enterprise.users.add(user)
        enterprise.save()

        return Response({
            'success': 'true',
            'message': '收藏成功'
        })


# 取消收藏公司
class CancleCollectCompanyView(GenericAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseModelSerializer
    lookup_field = 'id'
    lookup_url_kwarg = lookup_field
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, id, *args, **kwargs):
        enterprise = self.get_queryset().get(id=id)
        user = self.get_object()

        enterprise.users.remove(user)
        enterprise.save()

        return Response({
            'success': 'true',
            'message': '取消收藏成功'
        })


# 最新职位
class LastestRecruitView(ListAPIView, GenericAPIView):
    queryset = Recruit.objects.all().order_by('-createtime')
    serializer_class = LastestRecruitModelSerializer

    def post(self, request):
        cityname = request.data.get('cityname')
        kw = request.data.get('keyword')
        recruits = self.queryset.filter(city=cityname).filter(jobname__contains=kw)
        serializer = self.get_serializer(instance=recruits, many=True)

        return Response(serializer.data)
