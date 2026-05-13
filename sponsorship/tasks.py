from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging

from assesments.models import Assignment , Submission
from .models import *

logger = logging.getLogger(__name__)


@shared_task

def send_sponsor_progress_report():

  logger.info("Running progress Check")

  sponsorships = Sponsorship.objects.select_related(

      'sponsor',
      'enrollment__student',
      'enrollment__course',
  )

  for sponsorship in sponsorships:

    sponsor = sponsorship.sponsor
    enrollment = sponsorship.enrollment
    student = sponsorship.enrollment.student
    course = sponsorship.enrollment.course

    if not student.email:
      continue

    total_assignments = Assignment.objects.filter(course = course).count()
    submitted_assignment = Submission.objects.filter(assignment__course = course,student=student).count()
    missing_assignments = (total_assignments - submitted_assignment)
    progress = enrollment.progress


    try :
      send_mail(
        subject=f"Progress Report of {student.username}",
        message=(
          f"Student: {student.username}\n"
          f"Course: {course.title}\n"
          f"Progress: {progress}%\n"
          f"Enrollment status: {enrollment.status}\n"
          f"Assignment Submitted: {submitted_assignment}\n"
          f"Missing Assignment: {missing_assignments}\n"
    ),
        from_email='reply@demomailtrap.co',
        recipient_list=[sponsor.email],
        fail_silently=False,
)

      logger.info(
                f"Sponsor report sent | sponsor={sponsor.id}"
            )

    except Exception as e :
       logger.error(f"Sponsor report Failed : {e}",exc_info = True)

