from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
import requests

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
            if authorization_header.startswith('Bearer '):
                access_token = authorization_header.split(' ')[1]
                expiry_time = getattr(user, 'expiry_time', None)  # Assuming your token has an expiry time attribute
                if expiry_time:
                    # Check if the access token is about to expire
                    if expiry_time <= timezone.now() + timedelta(minutes=5):
                        # Token is about to expire, refresh it
                        new_access_token = self.refresh_access_token(getattr(user, 'refresh_token', None))
                        if new_access_token:
                            # Update the access token in the user object
                            setattr(user, 'access_token', new_access_token)
                        else:
                            # Failed to refresh token, return unauthorized response
                            return Response({"error": "Failed to refresh access token"}, status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response

    def get_refresh_token(refresh_token):
    
        refresh_url = settings.REFRESH_URL
        
        data={
            'refresh_token': refresh_token
        }
        
        response = requests.post(refresh_url, data=data)
        
        if response.status_code == 200:
            # Extract the new access token from the response
            new_access_token = response.json().get('access_token')
            return new_access_token
        else:
            # Token refresh failed, return None
            return None