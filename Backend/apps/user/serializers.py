from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import UserAccount

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'second_name',
            'last_name',
            'second_last_name',
            'is_active',
            'is_staff',
            'is_admin',
            'is_val',
            'is_digi',
            'is_terpel',
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'email', 
            'first_name', 
            'second_name', 
            'last_name', 
            'second_last_name',
            'is_admin', 
            'is_val', 
            'is_digi', 
            'is_terpel'
        ]
        extra_kwargs = {
            'is_admin': {'required': False},
            'is_val': {'required': False},
            'is_digi': {'required': False},
            'is_terpel': {'required': False},
        }