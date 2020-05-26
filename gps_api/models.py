from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=50)


class GPSFootprint(models.Model):
    lat = models.FloatField(verbose_name='latitude')
    lng = models.FloatField(verbose_name='longitude')
    published_at = models.DateTimeField()
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='gps_footprints')
