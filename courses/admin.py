from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model.
    
    Customized admin interface for managing courses with key fields displayed:
    title, description, instructor, difficulty level, dates, and publish status.
    """
    fields = (
        'title',
        'description',
        'instructor',
        'difficulty',
        'start_date',
        'duration_days',
        'is_published',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model.
    
    Allows administrators to view and manage student course enrollments,
    progress tracking, and enrollment status.
    """
    pass
