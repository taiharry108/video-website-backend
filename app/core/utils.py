import core.models as models
from datetime import date

from django.contrib.auth import get_user_model

def sample_show(**params):
    """Return sample show with default value"""
    defaults = {
        'name': 'Show 1',
        'num_seasons': 1,
        'num_eps': 10,
        'is_finished': False,
        'thum_img_url': "test.url",
        'rating': 4,
        'last_update': date.today()
    }

    defaults.update(params)
    return models.Show.objects.create(
        **defaults
    )


def sample_season(show, **params):
    """Return sample season with default value"""
    defaults = {
        'name': 'Season 1',
        'num_eps': 10,
        'show': show,
        'last_update': date.today()
    }

    defaults.update(params)
    return models.Season.objects.create(
        **defaults
    )


def sample_ep(season, **params):
    """Return sample ep with default value"""
    defaults = {
        'name': 'Ep 01',
        'show': season.show,
        'season': season,
        'idx': 0,
        'last_update': date.today()
    }
    defaults.update(params)
    return models.Ep.objects.create(
        **defaults
    )


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a simple user"""
    return get_user_model().objects.create_user(email, password)
