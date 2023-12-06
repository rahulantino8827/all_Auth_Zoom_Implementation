# Create your views here.
import requests
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

class GoogleAuthorize(APIView):
    def get(self,request):
        # Build the Zoom OAuth2 authorization URL
        google_authorization_url = 'https://accounts.google.com/o/oauth2/auth'
        params = {
            'response_type': 'code',
            # 'client_id': settings.ZOOM_CLIENT_ID,
            'client_id': "195961161874-0n8t0l6bif6tg9pj1531s8d21ureq905.apps.googleusercontent.com",
            'redirect_uri': 'https://www.google.com',  # Change to your callback URL
            'scope' : "openid email profile"
        }
        authorization_url = f'{google_authorization_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}'

        return Response({'authorization_url': authorization_url})

class GoogleCallback(APIView):
    def get(self,request):
        # Handle the Zoom OAuth2 callback here
        # authorization_code = request.GET.get('code')

        # if you want to generate token first time use below code here code is token which we get when url hits

        code = "4%2F0AfJohXlsaR2_1LrcbORE87xQkJP07ewnWQo2Tu1goM83SifcPfe2h1OvEcKR7scDAbONkQ"

        # if you want to generate token second time or more use below code here code is access token

        # code = "ya29.a0AfB_byDeQZ93XZOyWsos7HlpAeRP3RMktSP4co0yFZguo5G22H5WAvgmWwtxBSw4oZs8xvwW-gcIZ1L9aSpgcM0-7P41szoEHHRNDOpzq9qv0CMZbkPzfgmMv3aCIWYzk47QuFLTonfBubr_odFXWnbYz8vXW5ucmgaCgYKASsSARMSFQGOcNnCql5q9pyOhDmXEOYIl9KUJQ0169"
        if "%2F" in code:
            authorization_code = code.replace("%2F","/")
            print(authorization_code,"if")
            data = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': 'https://www.google.com',  # Change to your callback URL
                'client_id' : '195961161874-0n8t0l6bif6tg9pj1531s8d21ureq905.apps.googleusercontent.com',
                'client_secret': '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',
                'scope' : 'openid email profile'
            }
        else:
            authorization_code = code
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': authorization_code,
                'redirect_uri': 'https://www.google.com',  # Change to your callback URL
                'client_id' : '195961161874-0n8t0l6bif6tg9pj1531s8d21ureq905.apps.googleusercontent.com',
                'client_secret': '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',
                'scope' : 'openid email profile'
            }
            print(authorization_code,"else")

        # Exchange the authorization code for an access token
        google_token_url = 'https://oauth2.googleapis.com/token'
        response = requests.post(google_token_url, data=data)

        if response.status_code == 200:
            # Store the access token securely and handle Zoom API requests
            access_token = response.json().get('access_token')
            return Response({'access_token': access_token})
        else:
            return Response({'error': 'OAuth2 token exchange failed'}, status=response.status_code)
        

class get_user_details_from_google(APIView):

    def get(self,request):
        # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
        JWT_TOKEN = 'ya29.a0AfB_byDeQZ93XZOyWsos7HlpAeRP3RMktSP4co0yFZguo5G22H5WAvgmWwtxBSw4oZs8xvwW-gcIZ1L9aSpgcM0-7P41szoEHHRNDOpzq9qv0CMZbkPzfgmMv3aCIWYzk47QuFLTonfBubr_odFXWnbYz8vXW5ucmgaCgYKASsSARMSFQGOcNnCql5q9pyOhDmXEOYIl9KUJQ0169'

        # Define the API endpoint URL
        api_url = 'https://www.googleapis.com/oauth2/v2/userinfo'

        # Set the headers with the access token
        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        # Make a GET request to the API endpoint
        response =requests.get(
                                api_url,
                                headers=headers
                                )

        data = response.json()
        return Response({"data" : data})