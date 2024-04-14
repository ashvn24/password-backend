from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class CustomUser(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh' : str(refresh),
            'access': str(refresh.access_token)
        }