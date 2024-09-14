from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import LoginApiView, LogoutApiView

urlpatterns = [
    path('auth/login/', LoginApiView.as_view(), name='login'),  # User login endpoint
    path('auth/logout/', LogoutApiView.as_view(), name='logout'),  # User logout endpoint

    # JWT Token Endpoints
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh endpoint
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Token verify endpoint
]
