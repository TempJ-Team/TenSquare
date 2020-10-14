from rest_framework import serializers
from .models import *


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


