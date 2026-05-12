from celery import shared_task
from django.utils import timezone
from .models import Enrollment


@shared_task

def complete_expired_enrollments():
  now = timezone.now()
  updated = Enrollment.objects.filter(course__end_date__lte=now,status = 'act').update(status = 'com')
  return f"{updated}Enrollment marked as complete"