from rest_framework import serializers

from .models import GPSFootprint, Device


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    gps_footprints = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Device
        fields = '__all__'


class GPSFootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSFootprint
        fields = '__all__'
