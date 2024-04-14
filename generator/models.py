from django.db import models
from users.models import CustomUser

# Create your models here.

class SavePassword(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False,blank=False)
    password = models.CharField(max_length=50,null=False, blank=False)
    
    def __str__(self):
        return self.name