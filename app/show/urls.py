from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('shows', views.ShowViewSet)
router.register('seasons', views.SeasonViewSet)
router.register('eps', views.EpViewSet)

app_name = 'show'

urlpatterns = [
    path('', include(router.urls))
]
