from .models import Assignment, Submission, ReminderLog
from courses.models import Enrollment
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import logging


logger = logging.getLogger(__name__)


def check_deadlines_and_send_emails():
    logger.info("Checking Overdue Assignments")

    now = timezone.now()

    due_assignments = Assignment.objects.filter(
        due_date__gte=now,
        due_date__lte=now + timedelta(hours=1)
    )

    for assignment in due_assignments:
        logger.info(f"Processing assignment {assignment.id}")

        enrollments = Enrollment.objects.filter(course=assignment.course)

        for enrollment in enrollments:
            student = enrollment.student

            if not student.email:
                logger.warning(f"Skipping student={student.id} | reason=no_email")
                continue

            # check submission
            submitted = Submission.objects.filter(
                assignment=assignment,
                student=student
            ).exists()

            if submitted:
                logger.info(f"Skipping student={student.id} assignment={assignment.id} | reason=submitted")
                continue

            # get or create reminder log
            reminder, _ = ReminderLog.objects.get_or_create(
                student=student,
                assignment=assignment
            )

            # check if recently notified
            if reminder.last_reminder_sent_at:
                if now - reminder.last_reminder_sent_at < timedelta(hours=1):
                    logger.info(f"Skipping student={student.id} assignment={assignment.id} | reason=recently_notified")
                    continue

            # send email
            try:
                logger.info(
                    f"Sending email | student={student.id} assignment={assignment.id}"
                )

                send_mail(
                    subject=f"Assignment Due Soon: {assignment.title}",
                    message=f"The assignment '{assignment.title}' is due soon. Please submit it.",
                    from_email='reply@demomailtrap.co',
                    recipient_list=[student.email],
                    fail_silently=False,
                )

                # update timestamp
                reminder.last_reminder_sent_at = now
                reminder.save()

                logger.info(
                    f"Email sent successfully | student={student.id} assignment={assignment.id}"
                )

            except Exception:
                logger.error(
                    f"Failed to send email | student={student.id} assignment={assignment.id}",
                    exc_info=True
                )