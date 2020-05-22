from rest_framework import viewsets, mixins, status

from core.models import Show
from . import serializers
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class ShowViewSet(viewsets.ModelViewSet):
    """Manage Shows in database"""
    queryset = Show.objects.all()
    serializer_class = serializers.ShowSerializer
    authentication_classes = (TokenAuthentication, )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
