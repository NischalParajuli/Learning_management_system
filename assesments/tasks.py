"""Celery tasks for sending assignment and course reminders.

Periodic tasks that check for upcoming assignment deadlines and course
end dates, then sends email reminders to enrolled students.
"""

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging

from courses.models import Course, Enrollment
from .models import Assignment, Submission, ReminderLog

logger = logging.getLogger(__name__)


def should_send_reminder(reminder, now):
    """Check if enough time has passed to send another reminder.
    
    Prevents spam by checking if at least 1 hour has passed since the last reminder.
    Args:
        reminder: ReminderLog instance to check.
        now: Current datetime.
    Returns:
        bool: True if reminder should be sent, False otherwise.
    """
    if reminder.last_reminder_sent_at:
        # Only send if at least 1 hour has passed since last reminder
        return now - reminder.last_reminder_sent_at >= timedelta(hours=1)
    return True


def send_email(student, subject, message):
    """Send email to a student.
    Args:
        student: User instance to send email to.
        subject: Email subject line.
        message: Email body content.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email='reply@demomailtrap.co',
        recipient_list=[student.email],
        fail_silently=False,
    )


@shared_task
def check_assignment_deadlines():
    """Check for upcoming assignment deadlines and send reminders.
    
    Runs periodically to find assignments due within the next hour,
    then sends reminders to students who haven't submitted yet.
    
    Returns:
        None
    """
    logger.info("Running assignment + course reminder check")

    now = timezone.now()
    upcoming = now + timedelta(hours=1)

    # Find assignments due within the next hour
    assignments = Assignment.objects.filter(
        due_date__gte=now,
        due_date__lte=upcoming
    )

    for assignment in assignments:
        enrollments = Enrollment.objects.filter(course=assignment.course)

        for enrollment in enrollments:
            student = enrollment.student

            # Skip if student has no email
            if not student.email:
                continue

            # Skip if student already submitted
            if Submission.objects.filter(
                assignment=assignment,
                student=student
            ).exists():
                continue

            # Get or create reminder log to track sent reminders
            reminder, _ = ReminderLog.objects.get_or_create(
                student=student,
                assignment=assignment
            )

            if not should_send_reminder(reminder, now):
                continue

            try:
                send_email(
                    student,
                    subject=f"Assignment Due Soon: {assignment.title}",
                    message=f"Assignment '{assignment.title}' is due within 1 hour."
                )

                reminder.last_reminder_sent_at = now
                reminder.save()

                logger.info(f"Assignment email sent | student={student.id}")

            except Exception as e:
                logger.error(f"Assignment email failed: {e}", exc_info=True)

    # Find courses ending within the next day
    courses = Course.objects.filter(
        end_date__gte=now,
        end_date__lte=timezone.now() + timedelta(days=1)
    )

    for course in courses:
        enrollments = Enrollment.objects.filter(course=course)

        for enrollment in enrollments:
            student = enrollment.student

            if not student.email:
                continue

            reminder, _ = ReminderLog.objects.get_or_create(
                student=student,
                course=course
            )

            if not should_send_reminder(reminder, now):
                continue

            try:
                send_email(
                    student,
                    subject=f"Course Ending Soon: {course.title}",
                    message=f"Course '{course.title}' is ending soon."
                )

                reminder.last_reminder_sent_at = now
                reminder.save()

                logger.info(f"Course email sent | student={student.id}")

            except Exception as e:
                logger.error(f"Course email failed: {e}", exc_info=True)