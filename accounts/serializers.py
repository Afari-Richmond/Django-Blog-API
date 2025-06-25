# import serializers and User
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    # Validate the data
    def validate(self, data):

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User already exists')

        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            firstname = validated_data['firstname'],
            lastname =  validated_data['lastname'],
            username = validated_data['username']
        )

        user.set_password(validated_data['password'])

        return validated_data
