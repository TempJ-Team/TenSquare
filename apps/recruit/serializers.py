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
# 7.9,,7.10,,7.11使用的都是该序列化器
class EnterpriseModelSerializer(serializers.ModelSerializer):
    recruits = RecruitModelSerialier(many=True, required=False)

    class Meta:
        model = Enterprise
        fields = '__all__'
        extra_kwargs = {
            'users': {
                'allow_empty': True,
                'required': False
            }
        }

#7.1推荐职位(序列化器1）
class Recommend_RecruitModelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer()
    class Meta:
        model = Recruit
        fields = ['id','jobname','salary','condition','education','type',
                'city','createtime','enterprise','labels']

# 热门城市7.4
class Hot_CityModelSerialier(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


# 最新职位/搜索职位
class LastestRecruitModelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer()

    class Meta:
        model = Recruit
        fields = '__all__'












