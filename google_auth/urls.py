from django.urls import path
from .views import GoogleAuthorize,GoogleCallback,get_user_details_from_google


urlpatterns = [
    path('api/authorize/', GoogleAuthorize.as_view(), name='google_authorize'),
    path('api/callback/', GoogleCallback.as_view(), name='google_callback'),
    path('api/details/', get_user_details_from_google.as_view(), name='google_callback'),
]
