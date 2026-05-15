"""Serializers for Sponsorship models.

Provides serialization for Sponsorship and CourseSponsor models.
"""

from rest_framework import serializers

from .models import Sponsorship, CourseSponsor


class SponsorshipSerializer(serializers.ModelSerializer):
    """Serializes Sponsorship model instances to/from JSON.
    
    The sponsor and sponsored_at fields are read-only as they are set
    automatically by the system.
    """

    class Meta:
        model = Sponsorship
        fields = '__all__'
        read_only_fields = ['sponsor', 'sponsored_at']


class CourseSponsorSerializer(serializers.ModelSerializer):
    """Serializes CourseSponsor model instances to/from JSON."""

    class Meta:
        model = CourseSponsor
        fields = '__all__'