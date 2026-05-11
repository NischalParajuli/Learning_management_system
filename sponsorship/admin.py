from django.contrib import admin
from .models import Sponsorship , CourseSponsor
# Register your models here.


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
  pass

@admin.register(CourseSponsor)
class CourseSponsorAdmin(admin.ModelAdmin):
  pass