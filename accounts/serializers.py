# import serializers and User
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # Validate the data
    def validate(self, data):

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User already exists')

        return data
