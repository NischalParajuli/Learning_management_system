from django.contrib import admin
from .models import Sponsorship , CourseSponsor


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    """Admin configuration for Sponsorship model.
    
    Allows administrators to manage sponsor-student enrollment relationships
    and financial sponsorship tracking.
    """
    pass


@admin.register(CourseSponsor)
class CourseSponsorAdmin(admin.ModelAdmin):
    """Admin configuration for CourseSponsor model.
    
    Allows administrators to manage sponsor-course relationships and
    course-level sponsorship tracking.
    """
    pass