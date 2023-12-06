import requests
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

class zoom_authorize(APIView):
    def get(self,request):
        # Build the Zoom OAuth2 authorization URL
        zoom_authorization_url = 'https://zoom.us/oauth/authorize'
        params = {
            'response_type': 'code',
            # 'client_id': settings.ZOOM_CLIENT_ID,
            'client_id': "rvGr7cYJTE2Stat_4j5GjA",
            'redirect_uri': 'https://www.google.com/',  # Change to your callback URL
        }
        authorization_url = f'{zoom_authorization_url}?{"&".join([f"{key}={value}" for key, value in params.items()])}'

        return Response({'authorization_url': authorization_url})

class zoom_callback(APIView):
    def get(self,request):
        # Handle the Zoom OAuth2 callback here
        # authorization_code = request.GET.get('code')
        authorization_code = "l2rhjm54Zd8v1eUbhOLRwu2CfHOaDz8sQ"

        # Exchange the authorization code for an access token
        zoom_token_url = 'https://zoom.us/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'https://www.google.com/',  # Change to your callback URL
        }
        response = requests.post(zoom_token_url, data=data, auth=("rvGr7cYJTE2Stat_4j5GjA", "OhIKEXbrBFiMWjfmx4dJJp6HZSNr7mgl"))

        if response.status_code == 200:
            # Store the access token securely and handle Zoom API requests
            access_token = response.json().get('access_token')
            return Response({'access_token': access_token})
        else:
            return Response({'error': 'OAuth2 token exchange failed'}, status=response.status_code)


class get_user_details_from_zoom(APIView):

    def get(self,request):
        # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
        JWT_TOKEN = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjdjZTJiMGEwLTNkNTItNGY5OC04ODQyLTlkMDA3Y2Q1Yjg2YiJ9.eyJ2ZXIiOjksImF1aWQiOiJkODA3Y2RhNThkODlkNWViMjA3NTEyMmE5MjIyMDVkZSIsImNvZGUiOiJsMnJoam01NFpkOHYxZVViaE9MUnd1MkNmSE9hRHo4c1EiLCJpc3MiOiJ6bTpjaWQ6cnZHcjdjWUpURTJTdGF0XzRqNUdqQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJDdTV1UUxpWlJmcWdEbE13UmRMejJnIiwibmJmIjoxNjk2ODQwNTMwLCJleHAiOjE2OTY4NDQxMzAsImlhdCI6MTY5Njg0MDUzMCwiYWlkIjoiaDMtc0pNZFpRRXk3Z2E5RzVpMGppZyJ9.PgYKHow8U9eezZJgQ0TGVRG0tgQb6ddHYgkwCGOVl_vFutkydffmCCL5cDe8TDwBX7zKp0uWtQhMymHgqUmp0g'

        # Define the API endpoint URL
        api_url = 'https://api.zoom.us/v2/users/me'

        # Set the headers with the access token
        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        # Make a GET request to the API endpoint
        response =requests.get(
                                api_url,
                                headers=headers,
                                timeout=30)

        data = response.json()
        return Response({"data" : data})


class set_meeting_zoom(APIView):

    def post(self,request):
        # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
        JWT_TOKEN = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjdjZTJiMGEwLTNkNTItNGY5OC04ODQyLTlkMDA3Y2Q1Yjg2YiJ9.eyJ2ZXIiOjksImF1aWQiOiJkODA3Y2RhNThkODlkNWViMjA3NTEyMmE5MjIyMDVkZSIsImNvZGUiOiJsMnJoam01NFpkOHYxZVViaE9MUnd1MkNmSE9hRHo4c1EiLCJpc3MiOiJ6bTpjaWQ6cnZHcjdjWUpURTJTdGF0XzRqNUdqQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJDdTV1UUxpWlJmcWdEbE13UmRMejJnIiwibmJmIjoxNjk2ODQwNTMwLCJleHAiOjE2OTY4NDQxMzAsImlhdCI6MTY5Njg0MDUzMCwiYWlkIjoiaDMtc0pNZFpRRXk3Z2E5RzVpMGppZyJ9.PgYKHow8U9eezZJgQ0TGVRG0tgQb6ddHYgkwCGOVl_vFutkydffmCCL5cDe8TDwBX7zKp0uWtQhMymHgqUmp0g'

        # Define the API endpoint URL
        api_url = 'https://api.zoom.us/v2/users/me/meetings'

        # Set the headers with the access token
        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }
        meeting_data = {
            "topic": "testmeeting",
            "type":2,
            "start_time": "2023-06-15T12:10:10Z",
            "duration":"3",
            "settings":{
            "host_video":True,
            "participant_video":True,
            "join_before_host":True,
            "mute_upon_entry":"true",
            "watermark": "true",
            "audio": "voip",
            "auto_recording": "cloud"
                } 
  
             }
        # Make a GET request to the API endpoint
        requests.post(
                        api_url,
                        headers=headers,
                        data = meeting_data)

        return Response({"msg" : "meeting add successfully"})

class get_user_meeting_from_zoom(APIView):

    def get(self,request):
        # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
        JWT_TOKEN = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjdjZTJiMGEwLTNkNTItNGY5OC04ODQyLTlkMDA3Y2Q1Yjg2YiJ9.eyJ2ZXIiOjksImF1aWQiOiJkODA3Y2RhNThkODlkNWViMjA3NTEyMmE5MjIyMDVkZSIsImNvZGUiOiJsMnJoam01NFpkOHYxZVViaE9MUnd1MkNmSE9hRHo4c1EiLCJpc3MiOiJ6bTpjaWQ6cnZHcjdjWUpURTJTdGF0XzRqNUdqQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJDdTV1UUxpWlJmcWdEbE13UmRMejJnIiwibmJmIjoxNjk2ODQwNTMwLCJleHAiOjE2OTY4NDQxMzAsImlhdCI6MTY5Njg0MDUzMCwiYWlkIjoiaDMtc0pNZFpRRXk3Z2E5RzVpMGppZyJ9.PgYKHow8U9eezZJgQ0TGVRG0tgQb6ddHYgkwCGOVl_vFutkydffmCCL5cDe8TDwBX7zKp0uWtQhMymHgqUmp0g'

        # Define the API endpoint URL
        api_url = 'https://api.zoom.us/v2/users/me/meetings'

        # Set the headers with the access token
        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        # Make a GET request to the API endpoint
        response =requests.get(
                                api_url,
                                headers=headers,
                                timeout=30)

        data = response.json()
        return Response({"data" : data})