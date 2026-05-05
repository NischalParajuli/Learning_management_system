from .models import Assignment , Submission
from courses.models import Enrollment
from django.utils import timezone
from django.core.mail import send_mail

def check_deadlines_and_send_emails():

  due_assignments = Assignment.objects.filter(
    due_date__lt=timezone.now()
  )


  for assignment in due_assignments:
    enrollments = Enrollment.objects.filter(course = assignment.course)

    for enrollment in enrollments:
      student = enrollment.student

      submitted = Submission.objects.filter(
        assignment = assignment,
        student = student

      ).exists()


      if not submitted:
        send_mail(
          subject=f"Overdue Assignment: {assignment.title}",
          message=f"The assignment '{assignment.title}' is overdue. Please submit it ASAP.",
          from_email='reply@demomailtrap.co',
          recipient_list=[student.email],
          fail_silently=True,
        )
