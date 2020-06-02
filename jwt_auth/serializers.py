from datetime import datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import USER_SETTINGS


class TokenObtainPairAndLifetimeSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        now = int(datetime.now().timestamp())

        data['accessExpiresAt'] = now + USER_SETTINGS['ACCESS_TOKEN_LIFETIME'].total_seconds()
        data['refreshExpiresAt'] = now + USER_SETTINGS['REFRESH_TOKEN_LIFETIME'].total_seconds()

        return data


class TokenRefreshWithLifetimeSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        now = int(datetime.now().timestamp())

        data['accessExpiresAt'] = now + USER_SETTINGS['ACCESS_TOKEN_LIFETIME'].total_seconds()
        if 'refresh' in data:
            data['refreshExpiresAt'] = now + USER_SETTINGS['REFRESH_TOKEN_LIFETIME'].total_seconds()

        return data
