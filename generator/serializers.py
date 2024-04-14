from rest_framework import serializers
from .models import SavePassword

class PasswordSerializer(serializers.Serializer):
    length = serializers.IntegerField(min_value =6, max_value =15, default=12)
    lower_case = serializers.BooleanField(default=True)
    upper_case = serializers.BooleanField(default=True)
    digits = serializers.BooleanField(default=True)
    special_case = serializers.BooleanField(default=True)


class SavePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePassword
        fields =['id', 'name', 'password','user']
        extra_kwargs = {
            "user":{'required':False}
        }
        
    