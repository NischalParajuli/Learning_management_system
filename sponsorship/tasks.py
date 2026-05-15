"""Celery tasks for sending sponsor progress reports.

Periodic tasks that send progress reports to sponsors about their sponsored students.
"""

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging

from assesments.models import Assignment, Submission
from .models import *

logger = logging.getLogger(__name__)


@shared_task
def send_sponsor_progress_report():
    """Send progress reports to sponsors about their sponsored students.
    
    Retrieves all active sponsorships and sends email reports to sponsors
    showing their sponsored student's progress, assignments submitted,
    and missing assignments.
    
    Returns:
        None
    """
    logger.info("Running progress Check")

    # Fetch all sponsorships with related data to optimize queries
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

        # Skip if student has no email
        if not student.email:
            continue

        # Calculate assignment statistics
        total_assignments = Assignment.objects.filter(course=course).count()
        submitted_assignment = Submission.objects.filter(
            assignment__course=course,
            student=student
        ).count()
        missing_assignments = (total_assignments - submitted_assignment)
        progress = enrollment.progress

        try:
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

            logger.info(f"Sponsor report sent | sponsor={sponsor.id}")

        except Exception as e:
            logger.error(f"Sponsor report Failed : {e}", exc_info=True)

