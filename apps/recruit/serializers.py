'''
Descripition: 
Version: 
Author: SmartFox97
Date: 2020-10-13 23:06:59
LastEditors: SmartFox97
LastEditTime: 2020-10-13 23:10:05
'''
from rest_framework import serializers
from.models import *


#7.1.2（序列化器2）
class RecruitModelSerialier(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'

# 7.1.1(enterprise = models.ForeignKey)调用
class EnterpriseModelSerializer(serializers.ModelSerializer):
    recruits = RecruitModelSerialier(many=True)
    class Meta:
        model = Enterprise
        fields = '__all__'


#7.1推荐职位(序列化器1）
class Recommend_RecruitModelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer()
    class Meta:
        model = Recruit
        fields =['id','jobname','salary','condition','education','type',
                'city','createtime','enterprise','labels']


# 热门城市7.4
class Hot_CityModelSerialier(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'





