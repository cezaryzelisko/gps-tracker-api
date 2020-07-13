from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Device
from ..serializers import DeviceSerializer

DEVICE_LIST_URL = reverse('gps_api:device-list')
OBTAIN_TOKEN_URL = reverse('jwt_auth:token_obtain')


def get_device_detail_url(device_id):
    return reverse('gps_api:device-detail', args=[device_id])


class PrivateDeviceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User(username='testuser')
        self.user.set_password('testpass123')
        self.user.save()

        self.device = Device(name='testdevice', user=self.user)
        self.device.save()

    def test_cannot_create_device_unauthenticated(self):
        res = self.client.post(DEVICE_LIST_URL, {'name': 'testdevice', 'user': self.user})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_list_devices_unauthenticated(self):
        res = self.client.get(DEVICE_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_detail_device_unauthenticated(self):
        res = self.client.get(get_device_detail_url(self.device.pk))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_delete_device_unauthenticated(self):
        res = self.client.delete(get_device_detail_url(self.device.pk))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicDeviceTests(TestCase):
    def setUp(self):
        credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        self.user = self.create_user(**credentials)
        auth_header = self.get_access_token(credentials)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_header}')

    @staticmethod
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()

        return user

    def get_access_token(self, credentials):
        res = self.client.post(OBTAIN_TOKEN_URL, credentials)

        return res.data['access']

    def test_can_create_device(self):
        device_data = {
            'name': 'testdevice',
            'user': self.user
        }

        res = self.client.post(DEVICE_LIST_URL, device_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res.data)
        self.assertEqual(device_data['name'], res.data['name'])
        self.assertEqual(device_data['user'].pk, res.data['user'])

    def test_can_list_devices(self):
        _ = self.create_device('device1')
        _ = self.create_device('device2')
        _ = self.create_device('device3')

        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)

        res = self.client.get(DEVICE_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def create_device(self, name):
        device = Device(name=name, user=self.user)
        device.save()

        return device

    def test_can_get_device(self):
        device = self.create_device('testdevice')
        serializer = DeviceSerializer(device)

        res = self.client.get(get_device_detail_url(device.pk))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patch_device(self):
        device = self.create_device('testdevice')
        patch_data = {'name': 'patcheddevice'}

        res = self.client.patch(get_device_detail_url(device.pk), patch_data)

        updated_device = Device.objects.filter(id=device.pk)[0]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], updated_device.name)
