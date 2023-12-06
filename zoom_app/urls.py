from django.urls import path
from .views import zoom_authorize, zoom_callback,get_user_details_from_zoom,set_meeting_zoom,get_user_meeting_from_zoom

urlpatterns = [
    path('api/zoom/authorize/', zoom_authorize.as_view(), name='zoom_authorize'),
    path('api/zoom/callback/', zoom_callback.as_view(), name='zoom_callback'),
    path('api/zoom/getUserDetails/', get_user_details_from_zoom.as_view(), name='zoom_userdeatils'),
    path('api/zoom/addmeeting/', set_meeting_zoom.as_view(), name='addmeeting'),
    path('api/zoom/getmeeting/', get_user_meeting_from_zoom.as_view(), name='addmeeting'),
]
