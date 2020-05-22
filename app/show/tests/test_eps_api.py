from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ep
from ..serializers import EpSerializer
from core.utils import sample_season, sample_user, sample_show, sample_ep
from datetime import date

EPS_URL = reverse('show:ep-list')


def detail_url(season_id):
    """Return ep detail URL"""
    return reverse('show:ep-detail', args=[season_id])


class PublicSeasonApiTests(TestCase):
    """Test the publicly available eps API"""

    def setUp(self):
        self.client = APIClient()
        self.show = sample_show()
        self.season = sample_season(self.show)

    def test_no_login_required(self):
        """Test that no login is required for retrieving eps"""
        res = self.client.get(EPS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_eps(self):
        """Test retrieving eps"""
        sample_ep(self.season, name='ep 1')
        sample_ep(self.season, name='ep 2')
        sample_ep(self.season, name='ep 3')

        res = self.client.get(EPS_URL)

        eps = Ep.objects.all().order_by('name')

        serializer = EpSerializer(eps, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_ep(self):
        """Test retrieving an ep"""
        ep = sample_ep(self.season, name="Ep 1")
        sample_ep(self.season, name="Ep 2")

        res = self.client.get(detail_url(ep.id))
        serializer = EpSerializer(ep)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ep_failed(self):
        """Test that ep can't be created without authentication"""
        res = self.client.post(EPS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEpApiTests(TestCase):
    """Test the authorized user eps API"""

    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123',
            is_staff=True
        )

        self.client = APIClient()
        self.client.force_authenticate(self.admin_user)

    def test_create_ep_successful(self):
        """Test creating a new ep"""
        show = sample_show()
        season = sample_season(show)
        payload = {
            'name': 'ep 1',
            'idx': 10,
            'last_update': date.today(),
            'show': show.id,
            'season': season.id
        }

        res = self.client.post(EPS_URL, payload)

        exists = Ep.objects.filter(
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ep_invalid(self):
        """Test creating a new ep with invalid payload"""
        payload = {
            'name': '',
        }

        res = self.client.post(EPS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
