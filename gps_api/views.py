from rest_framework import viewsets

from .models import GPSFootprint, Device
from .serializers import GPSFootprintSerializer, DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GPSFootprintViewSet(viewsets.ModelViewSet):
    queryset = GPSFootprint.objects.all()
    serializer_class = GPSFootprintSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(device_id__user=self.request.user)

        if 'start_date' in self.request.query_params:
            queryset = queryset.filter(published_at__gte=self.request.query_params['start_date'])
        if 'end_date' in self.request.query_params:
            queryset = queryset.filter(published_at__lt=self.request.query_params['end_date'])

        return queryset
