"""Signal handlers for sending notification emails.

Connects to Django signals to automatically send emails when assignments
or quizzes are created or graded.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Submission, QuizSubmission, Assignment
from courses.models import Enrollment


@receiver(post_save, sender=Submission)
def notify_students_assignment_graded(sender, instance, **kwargs):
    """Send email to student when their assignment is graded.
    
    Triggered after a Submission is saved. Only sends email if the
    submission status changes to 'graded'.
    
    Args:
        sender: The model class (Submission).
        instance: The Submission instance being saved.
        **kwargs: Additional signal arguments.
    """
    # Only send if newly graded (status is 'grd')
    if instance.status == 'grd':
        return
    student = instance.student

    if not student.email:
        return
    
    try:
        send_mail(
            subject=f"Assignment Graded: {instance.assignment.title}",
            message=f"""Hi {student.username},

Your assignment '{instance.assignment.title}' has been graded.

Grade: {instance.grade}
Feedback: {instance.feedback or 'No feedback provided'}

Good luck!
""",
            from_email='reply@demomailtrap.co',
            recipient_list=[student.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email failed: {e}")


@receiver(post_save, sender=QuizSubmission)
def notify_student_quiz_graded(sender, instance, **kwargs):
    """Send email to student when their quiz submission is recorded.
    
    Triggered after a QuizSubmission is saved to notify the student
    that their quiz has been submitted and recorded.
    
    Args:
        sender: The model class (QuizSubmission).
        instance: The QuizSubmission instance being saved.
        **kwargs: Additional signal arguments.
    """
    student = instance.student

    if not student.email:
        return

    try:
        send_mail(
            subject=f"Quiz Results: {instance.quiz.title}",
            message=f"""Hi {student.username},

Your quiz '{instance.quiz.title}' has been submitted.

Score: {instance.score}

Good luck!
""",
            from_email='reply@demomailtrap.co',
            recipient_list=[student.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email failed: {e}")


@receiver(post_save, sender=Assignment)
def notify_student_new_assignments(sender, instance, created, **kwargs):
    """Send email to enrolled students when a new assignment is created.
    
    Triggered when a new Assignment is created. Notifies all students
    enrolled in the course about the new assignment.
    
    Args:
        sender: The model class (Assignment).
        instance: The Assignment instance being saved.
        created: Boolean indicating if this is a new instance.
        **kwargs: Additional signal arguments.
    """
    # Only process new assignments
    if not created:
        return
    
    enrollments = Enrollment.objects.filter(course=instance.course)

    for enrollment in enrollments:
        student = enrollment.student

        if not student.email:
            continue
        
        try:
            send_mail(
                subject=f"New Assignment: {instance.title}",
                message=f"""Hi {student.username},

A new assignment has been added to your course '{instance.course.title}'.

Assignment: {instance.title}
Due Date: {instance.due_date}

Good luck!
""",
                from_email='reply@demomailtrap.co',
                recipient_list=[student.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email failed: {e}")