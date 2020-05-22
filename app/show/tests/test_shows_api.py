from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Show
from ..serializers import ShowSerializer
from core.utils import sample_show, sample_user
from datetime import date

SHOWS_URL = reverse('show:show-list')


def detail_url(show_id):
    """Return show detail URL"""
    return reverse('show:show-detail', args=[show_id])


class PublicShowsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_no_login_required(self):
        """Test that no login is required for retrieving tags"""
        res = self.client.get(SHOWS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_shows(self):
        """Test retrieving shows"""
        sample_show(name='Show 1')
        sample_show(name='Show 2')
        sample_show(name='Show 3')

        res = self.client.get(SHOWS_URL)

        shows = Show.objects.all().order_by('name')

        serializer = ShowSerializer(shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_show(self):
        """Test retrieving a show"""
        show = sample_show(name="Show 1")
        sample_show(name="Show 2")

        res = self.client.get(detail_url(show.id))
        serializer = ShowSerializer(show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_show_failed(self):
        """Test that show can't be created without authentication"""
        res = self.client.post(SHOWS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShowsApiTests(TestCase):
    """Test the authorized user shows API"""

    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123',
            is_staff=True
        )

        self.client = APIClient()
        self.client.force_authenticate(self.admin_user)

    def test_create_show_successful(self):
        """Test creating a new show"""
        payload = {
            'name': 'Show 1',
            'num_seasons': 1,
            'num_eps': 10,
            'is_finished': False,
            'thum_img_url': "assets/gintama.jpg",
            'rating': 4,
            'last_update': date.today()
        }

        res = self.client.post(SHOWS_URL, payload)

        exists = Show.objects.filter(
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_show_invalid(self):
        """Test creating a new show with invalid payload"""
        payload = {
            'name': '',
        }

        res = self.client.post(SHOWS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
