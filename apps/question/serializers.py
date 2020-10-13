from rest_framework import serializers
from .models import *


# 个人提问
class LablesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'

class QuestionsModelSerializer(serializers.ModelSerializer):
    lables = LablesModelSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'