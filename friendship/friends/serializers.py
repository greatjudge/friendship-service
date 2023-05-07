from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest


User = get_user_model()


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
