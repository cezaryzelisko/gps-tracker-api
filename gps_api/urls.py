from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GPSFootprintViewSet, DeviceViewSet

router = DefaultRouter()
router.register('device', DeviceViewSet)
router.register('gps-footprint', GPSFootprintViewSet)

app_name = 'gps_api'
urlpatterns = [
    path('', include(router.urls))
]
