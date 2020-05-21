from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import date

from .. import models


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a simple user"""
    return get_user_model().objects.create_user(email, password)


def sample_show():
    return models.Show.objects.create(
        name='Show 1',
        num_seasons=1,
        num_eps=10,
        is_finished=False,
        thum_img_url="",
        rating=4,
        last_update=date.today()
    )


def sample_season(show):
    return models.Season.objects.create(
        name='Season 1',
        num_eps=10,
        show=show,
        last_update=date.today()
    )


def sample_ep(season):
    return models.Ep.objects.create(
        name='Ep 01',
        show=season.show,
        season=season,
        idx=0,
        last_update=date.today()
    )


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_show_str(self):
        """Test the show string representation"""
        show = sample_show()

        self.assertEqual(
            str(show), f"{show.name}:[{show.num_seasons}][{show.num_eps}]")

    def test_season_str(self):
        """Test the season string representation"""
        show = sample_show()
        season = sample_season(show)

        self.assertEqual(str(season),
                         f"{season.show.name} - {season.name} [{season.num_eps}]"
                         )

    def test_ep_str(self):
        """Test the ep string representation"""
        show = sample_show()
        season = sample_season(show)
        ep = sample_ep(season)

        self.assertEqual(str(ep),
                         f"{season.show.name} - {season.name} [{ep.name}]"
                         )
