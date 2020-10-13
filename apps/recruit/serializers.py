from rest_framework import serializers
from .models import *


class EnterpriseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = [
            'id',
            'name',
            'loge',
            'summary'
        ]


class RecruitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit
        fields = '__all__'
