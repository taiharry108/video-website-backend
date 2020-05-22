from rest_framework import serializers

from core.models import Show, Season, Ep


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


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for season objects"""

    class Meta:
        model = Season
        fields = (
            'id',
            'name',
            'last_update',
            'num_eps',
            'show',
        )
        read_only_fields = ('id', )


class EpSerializer(serializers.ModelSerializer):
    """Serializer for ep objects"""

    class Meta:
        model = Ep
        fields = (
            'id',
            'name',
            'last_update',
            'idx',
            'show',
            'season',
        )
        read_only_fields = ('id', )
