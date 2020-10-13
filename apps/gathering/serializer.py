from rest_framework import serializers
from .models import Gathering


class GatheringsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gathering
        fields = "__all__"


class GatherSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Gathering
        fields = ["id", "name", "image", "city", "starttime", "endrolltime", "users"]