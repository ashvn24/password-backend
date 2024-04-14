from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password','username']
        extra_kwargs ={
            'password':{'write_only':True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class LoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(max_length=200, read_only=True)
    refresh_token = serializers.CharField(max_length=200, read_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    class Meta:
        model =CustomUser
        fields=['email','password','access_token', 'refresh_token']
        extra_kwargs={
        "password": {"write_only": True},
        }
        
    def validate(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        request = self.context.get('request')
        
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credential')
        
        user_token = user.get_token()
        return{
            'email': user.email,
            'access_token':str(user_token.get('access')),
            'refresh_token':str(user_token.get('refresh'))
        }
        