from django.shortcuts import render
from rest_framework import generics,status
from .serializers import PasswordSerializer,SavePasswordSerializer
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SavePassword
# Create your views here.

class CreatePassword(generics.CreateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        length = data['length']
        upper = data['upper_case']
        lower = data['lower_case']
        digits = data['digits']
        special = data['special_case']
        
        if not (upper or  lower or digits or special):
            return Response({"error":"At least one character type must be selected."}, status=status.HTTP_400_BAD_REQUEST)
        
        charset = ''
        
        if lower:
            charset += 'abcdefghijklmnopqrstuvwxyz'
        if upper:
            charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if digits:
            charset += '0123456789'
        if special:
            charset +=  '!@#$%^&*()_+[]{}|;:,.<>?'
        
        password = get_random_string(length, charset)
        print(password)
        return Response({'password':password}, status=status.HTTP_201_CREATED)

class SavePasswordAPIView(generics.ListCreateAPIView):
    serializer_class = SavePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter the queryset based on the current user
        return SavePassword.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user field to the current authenticated user
        serializer.save(user=self.request.user)
        
        