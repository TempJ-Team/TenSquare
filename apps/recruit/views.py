from django.shortcuts import render
from django_rest.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
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
    # filter_fields = [
    #     'city',
    # ]

    # 搜索职位
    # TODO: 以上涉及职位序列化的可能缺少某些字段，回头检查
    def post(self, request):
        cityname = request.data.get('cityname')
        recruits = self.queryset.filter(city=cityname)
        serializer = self.get_serializer(instance=recruits, many=True)

        return Response(serializer.data)















