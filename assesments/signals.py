from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Submission, QuizSubmission , Assignment
from courses.models import Enrollment


@receiver(post_save , sender=Submission)

#sends emails to student when their assignment is graded
def notify_students_assignment_graded(sender,instance,**kwargs):

  #sends when status is graded
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

#sends email to students when their quiz submission is graded
@receiver(post_save, sender=QuizSubmission)
def notify_student_quiz_graded(sender, instance, **kwargs):
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


# sends email to students enrolled in the course when a new assignment is added
@receiver(post_save , sender=Assignment)

def notify_student_new_assignments(sender , instance, created , **kwargs):
    
    if not created:
        return
    
    enrollments = Enrollment.objects.filter(course=instance.course)

    for enrollment in enrollments:
        student = enrollment.student

        if not student.email:
            continue
        
        try : 
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