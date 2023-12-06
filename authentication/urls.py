"""
URL configuration for zoom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import Login_View,Get_Data_from_User,OTPSend,OTPVerification,ResetPassword,sendMail,ResetPasswordLinkVerifyView,ResetPasswordLinkView,EmailAPI



urlpatterns = [
    path("login/", Login_View.as_view()),
    path("user/", Get_Data_from_User.as_view()),
    path("otp/", OTPSend.as_view()),
    path("verification/", OTPVerification.as_view()),
    path("reset/",ResetPassword.as_view()),
    path("email/",sendMail.as_view()),
    path("reset-pass-link/",ResetPasswordLinkView.as_view()),
    path("changepass/",ResetPasswordLinkVerifyView.as_view()),
    path("htmlEmail/",EmailAPI.as_view()),

]
