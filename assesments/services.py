from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging

from courses.models import Course, Enrollment
from .models import Assignment, Submission, ReminderLog

logger = logging.getLogger(__name__)


def should_send_reminder(reminder, now):
    if reminder.last_reminder_sent_at:
        return now - reminder.last_reminder_sent_at >= timedelta(hours=1)
    return True


def send_email(student, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='reply@demomailtrap.co',
        recipient_list=[student.email],
        fail_silently=False,
    )


def check_assignment_deadlines():
    logger.info("Running assignment + course reminder check")

    now = timezone.now()
    upcoming = now + timedelta(hours=1)

    # ---------------- ASSIGNMENTS ----------------
    assignments = Assignment.objects.filter(
        due_date__gte=now,
        due_date__lte=upcoming
    )

    for assignment in assignments:
        enrollments = Enrollment.objects.filter(course=assignment.course)

        for enrollment in enrollments:
            student = enrollment.student

            if not student.email:
                continue

            if Submission.objects.filter(
                assignment=assignment,
                student=student
            ).exists():
                continue

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

    # ---------------- COURSES ----------------
    courses = Course.objects.filter(
        end_date__gte=now,
        end_date__lte= timezone.now() + timedelta(days=1)
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