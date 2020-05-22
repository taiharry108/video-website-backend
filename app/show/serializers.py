from rest_framework import serializers

from core.models import Show


class ShowSerializer(serializers.ModelSerializer):
    """Serializer for show objects"""

    class Meta:
        model = Show
        fields = (
            'id',
            'name',
            'last_update',
            'num_seasons',
            'num_eps',
            'thum_img_url',
            'banner_img_url',
            'rating',
            'is_finished'
        )
        read_only_fields = ('id', )
