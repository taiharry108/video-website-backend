from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Season
from ..serializers import SeasonSerializer
from core.utils import sample_season, sample_user, sample_show
from datetime import date

SEASONS_URL = reverse('show:season-list')


def detail_url(season_id):
    """Return season detail URL"""
    return reverse('show:season-detail', args=[season_id])


class PublicSeasonApiTests(TestCase):
    """Test the publicly available seasons API"""

    def setUp(self):
        self.client = APIClient()
        self.show = sample_show()

    def test_no_login_required(self):
        """Test that no login is required for retrieving seasons"""
        res = self.client.get(SEASONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_seasons(self):
        """Test retrieving seasons"""
        sample_season(self.show, name='season 1')
        sample_season(self.show, name='season 2')
        sample_season(self.show, name='season 3')

        res = self.client.get(SEASONS_URL)

        seasons = Season.objects.all().order_by('name')

        serializer = SeasonSerializer(seasons, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_season(self):
        """Test retrieving a season"""
        season = sample_season(self.show, name="Season 1")
        sample_season(self.show, name="Season 2")

        res = self.client.get(detail_url(season.id))
        serializer = SeasonSerializer(season)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_season_failed(self):
        """Test that season can't be created without authentication"""
        res = self.client.post(SEASONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSeasonApiTests(TestCase):
    """Test the authorized user seasons API"""

    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123',
            is_staff=True
        )

        self.client = APIClient()
        self.client.force_authenticate(self.admin_user)

    def test_create_season_successful(self):
        """Test creating a new season"""
        show = sample_show()
        payload = {
            'name': 'season 1',
            'num_eps': 10,
            'last_update': date.today(),
            'show': show.id
        }

        res = self.client.post(SEASONS_URL, payload)

        exists = Season.objects.filter(
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_season_invalid(self):
        """Test creating a new season with invalid payload"""
        payload = {
            'name': '',
        }

        res = self.client.post(SEASONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
