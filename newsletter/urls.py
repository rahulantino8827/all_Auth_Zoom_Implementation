from django.urls import path,include
from .views import NewsletterView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",NewsletterView.as_view()),
]+static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
