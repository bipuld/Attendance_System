from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['gender', 'phone', 'first_name', 'last_name', 'email', 'is_verify']
        read_only_fields = ['user'] 
