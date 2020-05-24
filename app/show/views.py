from rest_framework import viewsets, mixins, status, filters

from core.models import Show, Season, Ep, FeaturedShow
from . import serializers
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class ShowViewSet(viewsets.ModelViewSet):
    """Manage Shows in database"""
    queryset = Show.objects.all()
    serializer_class = serializers.ShowSerializer
    authentication_classes = (TokenAuthentication, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class FeaturedShowViewSet(viewsets.ModelViewSet):
    """Manage Featured Shows in database"""
    queryset = FeaturedShow.objects.all()
    serializer_class = serializers.FeaturedShowSerializer
    authentication_classes = (TokenAuthentication, )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class SeasonViewSet(viewsets.ModelViewSet):
    """Manage Seasons in database"""
    queryset = Season.objects.all()
    serializer_class = serializers.SeasonSerializer
    authentication_classes = (TokenAuthentication, )
    filterset_fields = ['show']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


class EpViewSet(viewsets.ModelViewSet):
    """Manage Seasons in database"""
    queryset = Ep.objects.all()
    serializer_class = serializers.EpSerializer
    authentication_classes = (TokenAuthentication, )
    filterset_fields = ['show']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
