"""Celery tasks for course completion tracking.

Periodic tasks that update enrollment statuses when course end dates pass.
"""

from celery import shared_task
from django.utils import timezone
from .models import Enrollment


@shared_task
def complete_expired_enrollments():
    """Mark enrollments as complete when their course ends.
    
    Finds all active enrollments whose course end date has passed
    and updates their status to 'complete'.
    
    Returns:
        str: Message indicating how many enrollments were updated.
    """
    now = timezone.now()
    # Update enrollments where course has ended and status is still 'active'
    updated = Enrollment.objects.filter(course__end_date__lte=now, status='act').update(status='com')
    return f"{updated}Enrollment marked as complete"