from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class LinkedInLogin(APIView):
    def get(self, request):
        client_id = "78umw301optzf3"

        url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri=https://oauth.pstmn.io/v1/callback&state=foobar&scope=openid%20profile%20w_member_social%20email"
        Json_response = {"Message" : "Successfully get Authorization_code...",
                         "Status" : status.HTTP_200_OK,
                         "Url" : url}
        return Response(Json_response)
    
    def post(self, request):
        code = request.data.get("code")
        
        requestfortoken = requests.post('https://www.linkedin.com/oauth/v2/accessToken',
                           data ={'grant_type':'authorization_code',
                                  "code": f"{code}",
                                  "client_id" : "78umw301optzf3",
                                  "client_secret" : "5kCdCrGYWIx4oyAJ",
                                  "redirect_uri" : "https://oauth.pstmn.io/v1/callback"
                                  })
        JWT_TOKEN = requestfortoken.json().get('access_token')        
        User_detail_url = "https://api.linkedin.com/v2/userinfo"
        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }
        requestforuserinfo =  requests.get(
                                            User_detail_url,
                                            headers=headers,
                                            timeout=30
                                        )
        result = requestforuserinfo.json()        
        return Response(result)