# import serializers and User
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    # Validate the data
    def validate(self, data):

        # checks the database to see if the user exists
        if User.objects.filter(username=data['username']).exists():
            # invokes the validate function in the serializer
            raise serializers.ValidationError('User already exists')
        # if validation fails, it raises an error

        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'].lower()
        )

        user.set_password(validated_data['password'])
        user.save() 

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  #define the data that the serializer will be expecting
    password = serializers.CharField()  # that is the username and password

    def validate(self, data):   # in the loginview, the validate logic is invoked when is_valid is hit

        if not User.objects.filter(username=data['username']).exists(): #checks if the user exists using the username
            raise serializers.ValidationError('account not found')  # rise an error if the validation fails

        return data   #otherwise, return the data from the user

    def get_jwt_token(self, data): 
        user = authenticate( # authenticate checks if the data passed is correct
            username=data['username'], password=data['password'])

        if not user:   #if authentication fails, output an error message
            return {'message': 'Invalid Credentials', 'data': {}}

        refresh = RefreshToken.for_user(user) # if details are correct, create a token
        return {'message': 'Login Success', 'data': {'token': {'refresh': str(refresh),
                                                               'access': str(refresh.access_token), }}}
