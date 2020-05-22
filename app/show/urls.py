from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('shows', views.ShowViewSet)

app_name = 'show'

urlpatterns = [
    path('', include(router.urls))
]
