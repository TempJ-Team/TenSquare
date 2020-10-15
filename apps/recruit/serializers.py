'''
Descripition: 
Version: 
Author: SmartFox97
Date: 2020-10-13 23:06:59
LastEditors: SmartFox97
LastEditTime: 2020-10-15 16:37:32
'''
from rest_framework import serializers
from.models import *


# 7.2.1(推荐职位)
class RecruitModelSerialier(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'

# 7.1.2(推荐职位)
class EnterpriseModelSerializer(serializers.ModelSerializer):
    recruits = RecruitModelSerialier(many=True, required=False)

    class Meta:
        model = Enterprise
        fields = '__all__'

#7.1.1(推荐职位)
class Recommend_RecruitModelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer(many=True)
    class Meta:
        model = Recruit
        fields ='__all__'


# 7.2.2(最新职位)
class Two_The_Latest_Job2ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'


#7.2.1(最新职位)
class One_The_Latest_JobModelSerialiazer(serializers.ModelSerializer):
    class Meta:
         model = Recruit
         fields = '__all__'


# 7.3.2(热门企业)
class Two_Hot_EnterpriseModelSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields ='__all__'

#7.3.1(热门企业)
class One_Hot_EnterpriseModelSerializer(serializers.ModelSerializer):
    recruits = EnterpriseModelSerializer(many=True)
    class Meta:
        model = Enterprise
        fields ='__all__'

#7.4热门城市
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










# # 7.5.2(搜索职位)
# class Two_Search_JobsModelSerializaer(serializers.ModelSerializer):
#     class Meta:
#         model = Recruit
#         fields = '__all__'
#
#
# # 7.5.1(搜索职位)
# class One_Search_JobsModelSerializer(serializers.ModelSerializer):
#     enterprise = EnterpriseModelSerializer(many=True)
#     class Meta:
#         model = Recruit
#         fields = '__all__'



# 7.6.3.1(职位详情）
class Three_Recruit_DetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'


# 7.6.2.2(职位详情）
class Two_Users_DetailModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

# 7.6.2.1(职位详情）
class Two_Recruit_Detail_ModelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer(many=True)
    class Meta:
        model = Recruit
        fields ='__all__'



# 7.6.1.2(职位详情）
class One_Users_DetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# 7.6.1(职位详情）
class One_Recruit_DetailModdelSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseModelSerializer(many=True)
    class Meta:
        model = Recruit
        fields = '__all__'



# 7.7增加职位访问次数
class Add_Recruit_VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'


# 7.8收藏职位
class Collection_RecruitSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recruit
        fieids = '__all__'

















