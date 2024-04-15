from django.shortcuts import render
from rest_framework import generics,status
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
# Create your views here.

class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'data': response.data,
        }, status=status.HTTP_201_CREATED)
        

class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    