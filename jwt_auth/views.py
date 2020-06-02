from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import TokenObtainPairAndLifetimeSerializer, TokenRefreshWithLifetimeSerializer


class TokenObtainPairAndLifetimeView(TokenObtainPairView):
    serializer_class = TokenObtainPairAndLifetimeSerializer


class TokenRefreshWithLifetimeView(TokenRefreshView):
    serializer_class = TokenRefreshWithLifetimeSerializer
