from django.urls import path, include

from .views import TokenObtainPairAndLifetimeView, TokenRefreshWithLifetimeView

app_name = 'jwt_auth'
urlpatterns = [
    path('', include('rest_framework.urls')),
    path('token/', TokenObtainPairAndLifetimeView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshWithLifetimeView.as_view(), name='token_refresh'),
]
