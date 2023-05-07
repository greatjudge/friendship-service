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
        fields = ['user_to', 'user_from', 'status']
        read_only_fields = ['status']

    def validate(self, attrs):
        if attrs['user_to'] == attrs['user_from']:
            raise serializers.ValidationError('user cant send request to self')
        return attrs
