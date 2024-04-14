from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreatePassword.as_view()),
    path('save/',  SavePasswordAPIView.as_view()),
]
