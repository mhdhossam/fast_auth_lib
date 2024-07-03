import uuid
from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from cryptography.fernet import Fernet
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')

        # Encrypt and store refresh token in cache
        fernet = Fernet(settings.MY_AUTH_LIB['FERNET_KEY'])
        encrypted_refresh_token = fernet.encrypt(refresh_token.encode())
        cache.set(encrypted_refresh_token, uuid.uuid4().hex, timeout=settings.MY_AUTH_LIB['REFRESH_TOKEN_LIFETIME'].total_seconds())
        logger.info(f'User {request.user.username} obtained tokens')

        return response

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        fernet = Fernet(settings.MY_AUTH_LIB['FERNET_KEY'])
        encrypted_refresh_token = fernet.encrypt(refresh_token.encode())

        if not cache.get(encrypted_refresh_token):
            return Response({"error": "Invalid or expired refresh token"}, status=400)

        # Delete old token and set new one
        cache.delete(encrypted_refresh_token)
        new_refresh_token = uuid.uuid4().hex
        encrypted_new_refresh_token = fernet.encrypt(new_refresh_token.encode())
        cache.set(encrypted_new_refresh_token, uuid.uuid4().hex, timeout=settings.MY_AUTH_LIB['REFRESH_TOKEN_LIFETIME'].total_seconds())

        response = super().post(request, *args, **kwargs)
        response.data['refresh'] = new_refresh_token
        logger.info(f'Refresh token rotated for user {request.user.username}')

        return response

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            fernet = Fernet(settings.MY_AUTH_LIB['FERNET_KEY'])
            encrypted_refresh_token = fernet.encrypt(refresh_token.encode())
            cache.delete(encrypted_refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f'User {request.user.username} logged out')
            return Response(status=204)
        except Exception as e:
            logger.error(f'Error logging out user {request.user.username}: {str(e)}')
            return Response({"error": "Invalid token"}, status=400)
