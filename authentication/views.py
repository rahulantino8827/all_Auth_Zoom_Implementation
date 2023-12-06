from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MyUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password,make_password
from .services import Util,send_email
import math
import random
from datetime import timedelta
from django.utils import timezone
from .models import OTP
from django.utils import timezone
from django.core.mail import send_mail
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }



class Login_View(APIView):

    def post(self,request):
        email = request.data["email"]
        password = request.data["password"]
        my_user = MyUser.objects.values_list("email",flat=True)
        if email in my_user:
            user = authenticate(request, username=email, password=password)
        else:

            return Response({
                "status" : 202,
                "msg" : "Kindly Register your email"
            })
        print(user,"kjhgfds")
        token = get_tokens_for_user(user)
        return Response({
            "status" : 200,
            "msg" : "User loggedIn successfully",
            "token" : token
        })
    


class Get_Data_from_User(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        data = MyUser.objects.values_list("email",flat=True)
        return Response({
            "status" : 200,
            "data" : data
        })
    


class OTPSend(APIView):

    def post(self,request):

        email = request.data["email"]
        users = MyUser.objects.filter(email=email)
        if len(users)> 0:
            digits = "0123456789"
            otp_code = "".join(digits[math.floor(random.random() * 10)] for _ in range(6))
            expiration_time = timezone.now() + timedelta(minutes=10)
            try:     
                OTP.objects.create(user=users[0],otp=otp_code,expiration_time=expiration_time)
            except:
                OTP.objects.get(user=users[0]).delete()
                OTP.objects.create(user=users[0],otp=otp_code,expiration_time=expiration_time)


            email_data = {
                        "subject": "One-Time Password (OTP) for Elchemy Password Reset",
                        "body": f"You recently requested to reset your password for the Elchemy.\nPlease use the following OTP to complete the password reset process:\nOTP: : {otp_code}",
                        "to_email": email,
                    }
            print(otp_code)
            Util.send_mail(data=email_data)
            return Response({
                    "status" : 200,
                    "msg" : "OTP Send Successfully. Please Check Your Mail"
                    })
        else:
            return Response({
                    "status" : 200,
                    "msg" : "Please Enter Registered Mail"
                    })
    
class OTPVerification(APIView):

    def post(self,request):
        
        email = request.data["email"]
        otp = request.data["otp"]
        user_id = MyUser.objects.get(email=email).id
        otp_obj = OTP.objects.get(user=user_id)
        otp_no  = otp_obj.otp
        otp_exp = otp_obj.expiration_time
        if str(otp_no) == str(otp):
            if otp_exp > timezone.now():
                otp_obj.is_verified = True
                otp_obj.save()
                return Response({
                    "status" : 200,
                    "msg" : "OTP Verified Sucessfully"
                })
            else:
                 return Response({
                    "status" : 200,
                    "msg" : "OTP Expired Please Resend OTP"
                })
        else:
            return Response({
                    "status" : 200,
                    "msg" : "Please Enter correct OTP"
                })


class ResetPassword(APIView):

    def post(self,request):

        email = request.data["email"]
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        try:
            if password1 == password2 :
                user_obj = MyUser.objects.get(email=email)
                user_id = user_obj.id
                otp_obj = OTP.objects.get(user=user_id)
                if otp_obj.is_verified == True:
                    user_obj.password = make_password(password1)
                    user_obj.save()
                    return Response({
                        "status" : 200,
                        "msg" : "Your Password Changed Successfully"
                    })
        except Exception as e:
            return Response({
                "status" : 200,
                "msg" : str(e)
            })
            


class sendMail(APIView):

    def get(self,request):

        email_data = {
                        "subject": "One-Time Password (OTP) for Elchemy Password Reset",
                        "body": "You recently requested to reset your password for the Elchemy.\nPlease use the following OTP to complete the password reset process:\nOTP",
                        "to_email": "vaibhav.s@antino.com",
                    }
        
        send_email(data=email_data)
        return Response({
            "status" : 200,
            "msg" : "mail send "
        })
    

class ResetPasswordLinkView(APIView):

    def post(self,request):
        email = request.data["email"]
        users = MyUser.objects.filter(email=email)
        if len(users)> 0:
            digits = "0123456789"
            otp_code = "".join(digits[math.floor(random.random() * 10)] for _ in range(6))
            expiration_time = timezone.now() + timedelta(minutes=10)
            try:     
                OTP.objects.create(user=users[0],otp=otp_code,expiration_time=expiration_time)
            except:
                OTP.objects.get(user=users[0]).delete()
                OTP.objects.create(user=users[0],otp=otp_code,expiration_time=expiration_time)


            email_data = {
                        "subject": "Raset password link for Elchemy Password Reset",
                        "body": f"You recently requested to reset your password for the Elchemy.\nPlease use the following link http://127.0.0.1:8000/auth/changepass/?email={email}&otp={otp_code} for reset password. ",
                        "to_email": email,
                    }
            print(otp_code)
            Util.send_mail(data=email_data)
            return Response({
                    "status" : 200,
                    "msg" : "Reset Password link sent Successfully. Please Check Your Mail"
                    })
        else:
            return Response({
                    "status" : 200,
                    "msg" : "Please Enter Registered Mail"
                    })


class ResetPasswordLinkVerifyView(APIView):

    def post(self,request):

        email = request.GET.get("email")
        otp = request.GET.get("otp")
        password1= request.data["password1"]
        password2= request.data["password2"]
        user_obj = MyUser.objects.get(email=email)
        user_id = user_obj.id
        otp_obj = OTP.objects.get(user=user_id)
        otp_no  = otp_obj.otp
        otp_exp = otp_obj.expiration_time
        if str(otp_no) == str(otp):
            if otp_exp > timezone.now():
                otp_obj.is_verified = True
                otp_obj.save()
                if password1==password2:
                    user_obj.password = make_password(password1)
                    user_obj.save()
                    return Response({
                        "status" : 200,
                        "msg" : "Password Changed Successfully."
                    })
        else:
            return Response({
                "status" : 200, 
                "msg" : "Link Expired Please resend link."
            })
        



class EmailAPI(APIView):
    def get(self, request):
        subject = self.request.GET.get('subject')
        txt_ = self.request.GET.get('text')
        html_ = self.request.GET.get('html')
        recipient_list = self.request.GET.get('recipient_list')
        from_email = "hitachipmei@gmail.com"

        if subject is None and txt_ is None and html_ is None and recipient_list is None:
            return Response({'msg': 'There must be a subject, a recipient list, and either HTML or Text.'}, status=200)
        elif html_ is not None and txt_ is not None:
            return Response({'msg': 'You can either use HTML or Text.'}, status=200)
        elif html_ is None and txt_ is None:
            return Response({'msg': 'Either HTML or Text is required.'}, status=200)
        elif recipient_list is None:
            return Response({'msg': 'Recipient List required.'}, status=200)
        elif subject is None:
            return Response({'msg': 'Subject required.'}, status=200)
        else:
            sent_mail = send_mail(
                subject,
                txt_,
                from_email,
                recipient_list.split(','),
                html_message=html_,
                fail_silently=False,
            )
            return Response({'msg': sent_mail}, status=200)
        

# url = http://127.0.0.1:8000/auth/htmlEmail/?subject=subject test&recipient_list=rahul.s@antino.com&html=<head>
#     <title>Image Display</title>
# </head>
# <body>
#     <h1>Hey Shubham bro You want this type of image</h1>
#     <a href="https://ibb.co/QcMPzZG"><img src="https://i.ibb.co/26dvmwB/jkimg.jpg" alt="jkimg" border="0"></a>
# </body>

