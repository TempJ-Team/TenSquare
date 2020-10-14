from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Spit
from rest_framework_jwt.utils import jwt_payload_handler,jwt_encode_handler


class SpitSimpleSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(required=False,allow_null=True)
    class Meta:
        model = Spit
        fields ='__all__'


