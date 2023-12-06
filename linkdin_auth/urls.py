from django.urls import path
from .views import LinkedInLogin


urlpatterns = [
    path('login/', LinkedInLogin.as_view(), name="LinkedIn"),
    ]

