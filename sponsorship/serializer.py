from rest_framework import serializers
from .models import Sponsorship , CourseSponsor


class SponsorshipSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sponsorship
    fields ='__all__'
    read_only_fields = ['sponsor','sponsored_at']

class CourseSponsorSerializer(serializers.ModelSerializer):
  class Meta:
    model = CourseSponsor
    fields = '__all__'

