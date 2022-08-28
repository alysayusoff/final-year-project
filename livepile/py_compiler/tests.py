from django.test import TestCase
from django.urls import reverse
from .models import *

class Py_Compiler_Test(TestCase):
    good_url = None
    bad_data = None
    data1 = None
    data2 = None
    data3 = None

    def setUp(self):
        self.good_url = reverse('room')
        self.bad_url = 'room'
        self.data1 = { 'room_name': 'room', 'username': ''}
        self.data2 = { 'room_name': 'room', 'username': 'user' }
        self.data3 = { 'room_name': 'room', 'username': 'user', 'password': 'password' }

    def tearDown(self):
        Room.objects.all().delete()

    def test_Room1Success(self):
        response = self.client.post(self.good_url, self.data1)
        self.assertEqual(response.status_code, 200)

    def test_Room2Success(self):
        response = self.client.post(self.good_url, self.data2)
        self.assertEqual(response.status_code, 200)

    def test_Room3Success(self):
        response = self.client.post(self.good_url, self.data3)
        self.assertEqual(response.status_code, 200)
        
    def test_RoomFailure(self):
        response = self.client.post(self.bad_url)
        self.assertEqual(response.status_code, 404)