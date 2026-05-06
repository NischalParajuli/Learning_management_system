from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'description',
        'instructor',
        'difficulty',
        'start_date',
        'duration_days',
        'is_published',
    )


admin.site.register(Enrollment)
