from rest_framework import viewsets

from .models import GPSFootprint, Device
from .serializers import GPSFootprintSerializer, DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GPSFootprintViewSet(viewsets.ModelViewSet):
    queryset = GPSFootprint.objects.all()
    serializer_class = GPSFootprintSerializer

    def get_queryset(self):
        return GPSFootprint.objects.filter(device_id__user=self.request.user)
