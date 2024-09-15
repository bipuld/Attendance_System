import logging

from django.conf import settings
from django.contrib.auth import authenticate ,login as django_login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


from .models import UserInfo
from .serializers import UserInfoSerializer

from attendance_sys import global_msg
from django.contrib import messages
# Create your views here.
logger = logging.getLogger('django')
class LoginApiView(APIView):
    """
    API endpoint for user login. This allow us to Login the user.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Render the login template.
        """
        return render(request, 'account/login.html') 

    def post(self, request):
        """
        Returns:
        - JsonResponse: JSON response with user data (username , refresh_token,access_token ) or error message.
        """
        # print("request.data",request.data)
        try:
            email= request.data['email'].lower()
            password = request.data['password']
        except KeyError as e:
            
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: 'Missing email or password in request data.',
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            try:
                
                user_info_details = UserInfo.objects.filter(user=user).first()
                
                if not user_info_details:
                    raise UserInfo.DoesNotExist  # Raise an error if UserInfo does not exist
            except UserInfo.DoesNotExist:
              
                messages = {
                    global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                    global_msg.ERROR_KEY: 'User information not found.',
                }
                return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
           
            messages = {
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
            }

            # Log the user in (Django session management for web login)
            django_login(request, user)
            
            return JsonResponse(messages, status=status.HTTP_200_OK)
        else:
          
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: 'Invalid username or password.',
            }
            return JsonResponse(messages, status=status.HTTP_401_UNAUTHORIZED)

class LogoutApiView(APIView):
    """
    API endpoint for user logout. This allow us to logout the user.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        try:
            token = RefreshToken.for_user(user)
            token.blacklist()
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: "Refresh token revoked successfully."
            }
        except Token as e:
            messages = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.ERROR_KEY: str(e)
            }
            return JsonResponse(messages, status=status.HTTP_400_BAD_REQUEST)
        messages = {
            global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
            global_msg.RESPONSE_MESSAGE_KEY: "User logged out successfully",
          
        }
        return JsonResponse(messages, status=status.HTTP_200_OK)
