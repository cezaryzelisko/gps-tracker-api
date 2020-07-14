from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from ..models import GPSFootprint, Device
from ..serializers import GPSFootprintSerializer

GPS_FOOTPRINT_LIST_URL = reverse('gps_api:gpsfootprint-list')
OBTAIN_TOKEN_URL = reverse('jwt_auth:token_obtain')


def get_gps_footprint_detail_url(gps_footprint_id):
    return reverse('gps_api:gpsfootprint-detail', args=[gps_footprint_id])


def get_current_datetime_as_formatted_string():
    default_datetime_str = str(timezone.localtime(timezone.now()))
    return 'T'.join(default_datetime_str.split())


class PrivateGPSFootprintTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User(username='testuser')
        self.user.set_password('testpass123')
        self.user.save()

        self.device = Device(name='testdevice', user=self.user)
        self.device.save()

        self.gps_footprint = GPSFootprint(
            lat=51.01,
            lng=21.01,
            published_at=get_current_datetime_as_formatted_string(),
            device_id=self.device
        )
        self.gps_footprint.save()

    def test_cannot_create_gps_footprint_unauthenticated(self):
        gps_footprint_data = {
            'lat': 51.10,
            'lng': 21.10,
            'published_at': get_current_datetime_as_formatted_string(),
            'device_id': self.device
        }
        res = self.client.post(GPS_FOOTPRINT_LIST_URL, gps_footprint_data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_list_gps_footprints_unauthenticated(self):
        res = self.client.get(GPS_FOOTPRINT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_detail_gps_footprint_unauthenticated(self):
        res = self.client.get(get_gps_footprint_detail_url(self.gps_footprint.pk))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_delete_gps_footprint_unauthenticated(self):
        res = self.client.delete(get_gps_footprint_detail_url(self.gps_footprint.pk))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicGPSFootprintTests(TestCase):
    def setUp(self):
        credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        self.user = self.create_user(**credentials)
        self.device = self.create_device(self.user)
        auth_header = self.get_access_token(credentials)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_header}')

    @staticmethod
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()

        return user

    @staticmethod
    def create_device(user):
        device = Device(name='testdevice', user=user)
        device.save()

        return device

    def get_access_token(self, credentials):
        res = self.client.post(OBTAIN_TOKEN_URL, credentials)

        return res.data['access']

    def test_can_create_gps_footprint(self):
        gps_footprint_data = {
            'lat': 51.10,
            'lng': 21.10,
            'published_at': get_current_datetime_as_formatted_string(),
            'device_id': self.device.pk
        }

        res = self.client.post(GPS_FOOTPRINT_LIST_URL, gps_footprint_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res.data)
        for key, value in gps_footprint_data.items():
            self.assertEqual(value, res.data[key])

    def test_can_list_gps_footprints(self):
        _ = self.create_gps_footprint(51.01, 21.01)
        _ = self.create_gps_footprint(51.03, 21.02)
        _ = self.create_gps_footprint(51.02, 21.03)

        gps_footprints = GPSFootprint.objects.all()
        serializer = GPSFootprintSerializer(gps_footprints, many=True)

        res = self.client.get(GPS_FOOTPRINT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def create_gps_footprint(self, lat, lng, published_at=timezone.now()):
        gps_footprint = GPSFootprint(lat=lat, lng=lng, published_at=published_at, device_id=self.device)
        gps_footprint.save()

        return gps_footprint

    def test_can_get_gps_footprint(self):
        gps_footprint = self.create_gps_footprint(51.01, 21.01)
        serializer = GPSFootprintSerializer(gps_footprint)

        res = self.client.get(get_gps_footprint_detail_url(gps_footprint.pk))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_can_patch_gps_footprint(self):
        gps_footprint = self.create_gps_footprint(51.01, 21.01)
        patch_data = {'lat': 52.01}

        res = self.client.patch(get_gps_footprint_detail_url(gps_footprint.pk), patch_data)

        updated_device = GPSFootprint.objects.filter(id=gps_footprint.pk)[0]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['lat'], updated_device.lat)

    def test_can_filter_gps_footprints_by_date(self):
        gps_footprint1 = self.create_gps_footprint(51.01, 21.01, timezone.make_aware(timezone.datetime(2020, 1, 1)))
        gps_footprint2 = self.create_gps_footprint(51.02, 21.02, timezone.make_aware(timezone.datetime(2020, 2, 1)))
        gps_footprint3 = self.create_gps_footprint(51.03, 21.03, timezone.make_aware(timezone.datetime(2020, 3, 1)))

        serializer1 = GPSFootprintSerializer(gps_footprint1)
        serializer2 = GPSFootprintSerializer(gps_footprint2)
        serializer3 = GPSFootprintSerializer(gps_footprint3)

        res = self.client.get(
            GPS_FOOTPRINT_LIST_URL,
            {
                'start_date': timezone.make_aware(timezone.datetime(2020, 2, 1)),
                'end_date': timezone.make_aware(timezone.datetime(2020, 2, 21))
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
